from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5)
    company: str = Field(default="")


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    company: str = ""
    api_key: str = Field(default_factory=lambda: f"sk-seed-user-{uuid.uuid4().hex[:24]}")
    agents: list[str] = Field(default_factory=list)
    workflows: list[str] = Field(default_factory=list)
    plan: str = Field(default="free")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
