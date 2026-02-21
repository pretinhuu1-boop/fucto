"""
Agent Factory - Creates personalized agents from workflow results.
Transforms pain points and ecosystem designs into ready-to-use agents.
"""
from app.models.agent import (
    Agent,
    AgentType,
    AgentStatus,
    AgentPersonality,
    AgentCapability,
)
from app.models.workflow import (
    Workflow,
    PainPoint,
    AgentBlueprint,
    EcosystemDesign,
)
from app.services.database import db


AGENT_TYPE_MAP = {
    "analyst": AgentType.ANALYST,
    "legal": AgentType.LEGAL,
    "collector": AgentType.COLLECTOR,
    "financial": AgentType.FINANCIAL,
    "judicial": AgentType.JUDICIAL,
    "orchestrator": AgentType.ORCHESTRATOR,
    "assistant": AgentType.ASSISTANT,
}


def create_agent_from_blueprint(
    blueprint: AgentBlueprint,
    workflow: Workflow,
    owner_id: str = "",
) -> Agent:
    agent_type = AGENT_TYPE_MAP.get(
        blueprint.role.lower(), AgentType.CUSTOM
    )

    responsibilities_text = "\n".join(f"- {r}" for r in blueprint.responsibilities)
    triggers_text = "\n".join(f"- {t}" for t in blueprint.triggers)
    outputs_text = "\n".join(f"- {o}" for o in blueprint.outputs)

    system_prompt = f"""You are {blueprint.name}, a specialized AI agent.

ROLE: {blueprint.description}

RESPONSIBILITIES:
{responsibilities_text}

TRIGGERS (when to act):
{triggers_text}

OUTPUTS (what you produce):
{outputs_text}

{"IMPORTANT: Some decisions require human approval. Always flag these clearly." if blueprint.human_checkpoint else "You operate autonomously within your defined scope."}
"""

    capabilities = []
    for resp in blueprint.responsibilities:
        capabilities.append(AgentCapability(
            name=resp[:50],
            description=resp,
            enabled=True,
        ))

    context = ""
    if workflow.discovery:
        context = (
            f"Client: {workflow.discovery.client_name}\n"
            f"Profession: {workflow.discovery.profession}\n"
            f"Business: {workflow.discovery.business_description}\n"
        )
    if workflow.pain_points:
        pain_text = "\n".join(
            f"- {p.title}: {p.description}" for p in workflow.pain_points
        )
        context += f"\nPain Points Being Addressed:\n{pain_text}"

    agent = Agent(
        name=blueprint.name,
        description=blueprint.description,
        agent_type=agent_type,
        status=AgentStatus.ACTIVE,
        system_prompt=system_prompt,
        personality=AgentPersonality(
            tone="professional",
            language="pt-BR",
            formality="formal",
            empathy_level=7,
        ),
        capabilities=capabilities,
        context=context,
        owner_id=owner_id,
    )

    return db.create_agent(agent)


def create_ecosystem_from_design(
    design: EcosystemDesign,
    workflow: Workflow,
    owner_id: str = "",
) -> list[Agent]:
    agents = []

    orchestrator = create_agent_from_blueprint(
        design.orchestrator, workflow, owner_id
    )
    agents.append(orchestrator)

    for blueprint in design.agents:
        agent = create_agent_from_blueprint(blueprint, workflow, owner_id)
        agents.append(agent)

    return agents


def create_quick_assistant(
    name: str,
    description: str,
    system_prompt: str,
    context: str = "",
    language: str = "pt-BR",
    tone: str = "professional",
    owner_id: str = "",
) -> Agent:
    agent = Agent(
        name=name,
        description=description,
        agent_type=AgentType.ASSISTANT,
        status=AgentStatus.ACTIVE,
        system_prompt=system_prompt,
        personality=AgentPersonality(
            tone=tone,
            language=language,
            formality="formal",
            empathy_level=7,
        ),
        context=context,
        owner_id=owner_id,
    )
    return db.create_agent(agent)
