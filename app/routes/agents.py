"""
Agent CRUD Routes - Create, read, update, delete agents.
"""
from fastapi import APIRouter, HTTPException
from typing import Optional

from app.models.agent import (
    Agent,
    AgentCreate,
    AgentUpdate,
    AgentStatus,
)
from app.services.database import db
from app.services.agent_factory import create_quick_assistant

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.get("/")
async def list_agents(owner_id: Optional[str] = None):
    agents = db.list_agents(owner_id)
    return {
        "agents": [a.model_dump() for a in agents],
        "total": len(agents),
    }


@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    agent = db.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent.model_dump()


@router.post("/")
async def create_agent(data: AgentCreate):
    agent = Agent(
        name=data.name,
        description=data.description,
        agent_type=data.agent_type,
        system_prompt=data.system_prompt,
        personality=data.personality,
        capabilities=data.capabilities,
        context=data.context,
        owner_id=data.owner_id,
        status=AgentStatus.ACTIVE,
    )
    created = db.create_agent(agent)
    return created.model_dump()


@router.post("/quick")
async def quick_create_agent(
    name: str,
    description: str = "Assistente personalizado",
    system_prompt: str = "Seja um assistente util e proativo.",
    context: str = "",
    language: str = "pt-BR",
    tone: str = "professional",
):
    agent = create_quick_assistant(
        name=name,
        description=description,
        system_prompt=system_prompt,
        context=context,
        language=language,
        tone=tone,
    )
    return agent.model_dump()


@router.put("/{agent_id}")
async def update_agent(agent_id: str, data: AgentUpdate):
    updates = data.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    agent = db.update_agent(agent_id, updates)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent.model_dump()


@router.delete("/{agent_id}")
async def delete_agent(agent_id: str):
    success = db.delete_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted", "id": agent_id}


@router.post("/{agent_id}/activate")
async def activate_agent(agent_id: str):
    agent = db.update_agent(agent_id, {"status": AgentStatus.ACTIVE.value})
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent activated", "agent": agent.model_dump()}


@router.post("/{agent_id}/pause")
async def pause_agent(agent_id: str):
    agent = db.update_agent(agent_id, {"status": AgentStatus.PAUSED.value})
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent paused", "agent": agent.model_dump()}


@router.get("/{agent_id}/stats")
async def agent_stats(agent_id: str):
    agent = db.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {
        "agent_id": agent.id,
        "name": agent.name,
        "status": agent.status.value,
        "total_conversations": agent.total_conversations,
        "total_messages": agent.total_messages,
        "telegram_linked": agent.telegram_linked,
        "created_at": agent.created_at,
    }
