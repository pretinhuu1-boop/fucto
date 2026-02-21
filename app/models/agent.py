from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid


class AgentType(str, Enum):
    ASSISTANT = "assistant"
    ANALYST = "analyst"
    LEGAL = "legal"
    COLLECTOR = "collector"
    FINANCIAL = "financial"
    JUDICIAL = "judicial"
    ORCHESTRATOR = "orchestrator"
    CUSTOM = "custom"


class AgentStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class AgentPersonality(BaseModel):
    tone: str = Field(default="professional", description="Communication tone")
    language: str = Field(default="pt-BR", description="Primary language")
    formality: str = Field(default="formal", description="Formality level")
    empathy_level: int = Field(default=7, ge=1, le=10, description="Empathy level 1-10")
    custom_instructions: str = Field(default="", description="Custom behavior instructions")


class AgentCapability(BaseModel):
    name: str
    description: str
    enabled: bool = True
    config: dict = Field(default_factory=dict)


class AgentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(default="")
    agent_type: AgentType = AgentType.ASSISTANT
    system_prompt: str = Field(default="")
    personality: AgentPersonality = Field(default_factory=AgentPersonality)
    capabilities: list[AgentCapability] = Field(default_factory=list)
    context: str = Field(default="", description="Business context and domain knowledge")
    owner_id: str = Field(default="")


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    personality: Optional[AgentPersonality] = None
    capabilities: Optional[list[AgentCapability]] = None
    context: Optional[str] = None
    status: Optional[AgentStatus] = None


class Agent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str = ""
    agent_type: AgentType = AgentType.ASSISTANT
    status: AgentStatus = AgentStatus.DRAFT
    system_prompt: str = ""
    personality: AgentPersonality = Field(default_factory=AgentPersonality)
    capabilities: list[AgentCapability] = Field(default_factory=list)
    context: str = ""
    owner_id: str = ""
    api_key: str = Field(default_factory=lambda: f"sk-seed-{uuid.uuid4().hex[:32]}")
    telegram_linked: bool = False
    telegram_chat_id: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    total_conversations: int = 0
    total_messages: int = 0


class AgentMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str


class AgentChatRequest(BaseModel):
    agent_id: str
    messages: list[AgentMessage]
    stream: bool = False


class AgentChatResponse(BaseModel):
    agent_id: str
    message: AgentMessage
    conversation_id: str
    usage: dict = Field(default_factory=dict)
