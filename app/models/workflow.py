from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid


class WorkflowPhase(str, Enum):
    DISCOVERY = "discovery"
    PAIN_MAPPING = "pain_mapping"
    AGENT_DESIGN = "agent_design"
    AGENT_CREATION = "agent_creation"
    TESTING = "testing"
    DELIVERY = "delivery"
    COMPLETED = "completed"


class WorkflowStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    WAITING_INPUT = "waiting_input"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class DiscoveryInput(BaseModel):
    client_name: str = Field(..., min_length=2)
    profession: str = Field(..., min_length=2)
    business_description: str = Field(default="")
    main_activities: list[str] = Field(default_factory=list)
    team_size: str = Field(default="solo")
    tech_comfort: str = Field(default="basic", description="basic, intermediate, advanced")


class PainPoint(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str
    description: str
    severity: int = Field(default=5, ge=1, le=10)
    category: str = Field(default="operational")
    ai_solvable: bool = True
    proposed_solution: str = ""


class AgentBlueprint(BaseModel):
    name: str
    role: str
    description: str
    responsibilities: list[str] = Field(default_factory=list)
    triggers: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    human_checkpoint: bool = False
    checkpoint_description: str = ""


class EcosystemDesign(BaseModel):
    orchestrator: AgentBlueprint
    agents: list[AgentBlueprint] = Field(default_factory=list)
    integrations: list[str] = Field(default_factory=list)
    human_checkpoints: list[str] = Field(default_factory=list)


class WorkflowCreate(BaseModel):
    client_name: str
    discovery: DiscoveryInput


class Workflow(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    phase: WorkflowPhase = WorkflowPhase.DISCOVERY
    status: WorkflowStatus = WorkflowStatus.IN_PROGRESS
    discovery: Optional[DiscoveryInput] = None
    pain_points: list[PainPoint] = Field(default_factory=list)
    ecosystem_design: Optional[EcosystemDesign] = None
    created_agents: list[str] = Field(default_factory=list)
    conversation_history: list[dict] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
