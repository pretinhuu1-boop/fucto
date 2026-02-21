"""
Workflow Routes - The discovery-to-delivery pipeline.
Guides users through understanding their business and creating personalized agents.
"""
from fastapi import APIRouter, HTTPException

from app.models.workflow import (
    Workflow,
    WorkflowCreate,
    WorkflowPhase,
    WorkflowStatus,
    PainPoint,
    AgentBlueprint,
    EcosystemDesign,
    DiscoveryInput,
)
from app.services.database import db
from app.services.ai_service import workflow_chat
from app.services.agent_factory import create_ecosystem_from_design

router = APIRouter(prefix="/api/workflows", tags=["workflows"])


@router.get("/")
async def list_workflows():
    workflows = db.list_workflows()
    return {
        "workflows": [w.model_dump() for w in workflows],
        "total": len(workflows),
    }


@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str):
    workflow = db.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow.model_dump()


@router.post("/")
async def create_workflow(data: WorkflowCreate):
    workflow = Workflow(
        client_name=data.client_name,
        discovery=data.discovery,
        phase=WorkflowPhase.DISCOVERY,
        status=WorkflowStatus.IN_PROGRESS,
    )
    created = db.create_workflow(workflow)
    return created.model_dump()


@router.post("/{workflow_id}/chat")
async def workflow_chat_endpoint(workflow_id: str, message: str):
    workflow = db.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    client_info = ""
    if workflow.discovery:
        client_info = (
            f"Name: {workflow.discovery.client_name}, "
            f"Profession: {workflow.discovery.profession}, "
            f"Business: {workflow.discovery.business_description}, "
            f"Activities: {', '.join(workflow.discovery.main_activities)}"
        )

    pain_info = ""
    if workflow.pain_points:
        pain_info = "; ".join(
            f"{p.title} (severity: {p.severity}/10)" for p in workflow.pain_points
        )

    history_text = ""
    if workflow.conversation_history:
        recent = workflow.conversation_history[-10:]
        history_text = "\n".join(
            f"{m['role']}: {m['content'][:200]}" for m in recent
        )

    response = await workflow_chat(
        phase=workflow.phase.value,
        client_info=client_info,
        pain_points=pain_info,
        history=history_text,
        user_message=message,
    )

    new_history = workflow.conversation_history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": response},
    ]
    db.update_workflow(workflow_id, {"conversation_history": new_history})

    return {
        "response": response,
        "phase": workflow.phase.value,
        "workflow_id": workflow_id,
    }


@router.post("/{workflow_id}/pain-points")
async def add_pain_points(workflow_id: str, pain_points: list[PainPoint]):
    workflow = db.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    existing = workflow.pain_points
    existing.extend(pain_points)

    db.update_workflow(workflow_id, {
        "pain_points": [p.model_dump() for p in existing],
        "phase": WorkflowPhase.PAIN_MAPPING.value,
    })

    return {"message": f"{len(pain_points)} pain points added", "total": len(existing)}


@router.post("/{workflow_id}/design")
async def set_ecosystem_design(workflow_id: str, design: EcosystemDesign):
    workflow = db.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    db.update_workflow(workflow_id, {
        "ecosystem_design": design.model_dump(),
        "phase": WorkflowPhase.AGENT_DESIGN.value,
    })

    return {"message": "Ecosystem design saved", "agents_planned": len(design.agents) + 1}


@router.post("/{workflow_id}/create-agents")
async def create_agents_from_workflow(workflow_id: str, owner_id: str = ""):
    workflow = db.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    if not workflow.ecosystem_design:
        raise HTTPException(status_code=400, detail="No ecosystem design found. Complete design phase first.")

    agents = create_ecosystem_from_design(
        workflow.ecosystem_design,
        workflow,
        owner_id=owner_id,
    )

    agent_ids = [a.id for a in agents]
    db.update_workflow(workflow_id, {
        "created_agents": agent_ids,
        "phase": WorkflowPhase.DELIVERY.value,
        "status": WorkflowStatus.COMPLETED.value,
    })

    return {
        "message": f"{len(agents)} agents created successfully",
        "agents": [{"id": a.id, "name": a.name, "api_key": a.api_key} for a in agents],
    }


@router.post("/{workflow_id}/advance")
async def advance_phase(workflow_id: str):
    workflow = db.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    phase_order = [
        WorkflowPhase.DISCOVERY,
        WorkflowPhase.PAIN_MAPPING,
        WorkflowPhase.AGENT_DESIGN,
        WorkflowPhase.AGENT_CREATION,
        WorkflowPhase.TESTING,
        WorkflowPhase.DELIVERY,
        WorkflowPhase.COMPLETED,
    ]

    current_idx = phase_order.index(workflow.phase)
    if current_idx < len(phase_order) - 1:
        next_phase = phase_order[current_idx + 1]
        db.update_workflow(workflow_id, {"phase": next_phase.value})
        return {"message": f"Advanced to {next_phase.value}", "phase": next_phase.value}

    return {"message": "Workflow already completed", "phase": workflow.phase.value}
