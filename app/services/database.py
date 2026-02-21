"""
In-memory database for MVP. Replace with SQLite/PostgreSQL for production.
"""
import json
import os
from typing import Optional

from app.models.agent import Agent
from app.models.workflow import Workflow
from app.models.user import User

DB_FILE = "seed_agents_data.json"


class Database:
    def __init__(self):
        self.agents: dict[str, Agent] = {}
        self.workflows: dict[str, Workflow] = {}
        self.users: dict[str, User] = {}
        self.conversations: dict[str, list[dict]] = {}
        self._load()

    def _load(self):
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, "r") as f:
                    data = json.load(f)
                for aid, adata in data.get("agents", {}).items():
                    self.agents[aid] = Agent(**adata)
                for wid, wdata in data.get("workflows", {}).items():
                    self.workflows[wid] = Workflow(**wdata)
                for uid, udata in data.get("users", {}).items():
                    self.users[uid] = User(**udata)
                self.conversations = data.get("conversations", {})
            except Exception:
                pass

    def _save(self):
        data = {
            "agents": {k: v.model_dump() for k, v in self.agents.items()},
            "workflows": {k: v.model_dump() for k, v in self.workflows.items()},
            "users": {k: v.model_dump() for k, v in self.users.items()},
            "conversations": self.conversations,
        }
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=2, default=str)

    # Agents
    def create_agent(self, agent: Agent) -> Agent:
        self.agents[agent.id] = agent
        self._save()
        return agent

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        return self.agents.get(agent_id)

    def get_agent_by_api_key(self, api_key: str) -> Optional[Agent]:
        for agent in self.agents.values():
            if agent.api_key == api_key:
                return agent
        return None

    def list_agents(self, owner_id: str = None) -> list[Agent]:
        if owner_id:
            return [a for a in self.agents.values() if a.owner_id == owner_id]
        return list(self.agents.values())

    def update_agent(self, agent_id: str, updates: dict) -> Optional[Agent]:
        agent = self.agents.get(agent_id)
        if not agent:
            return None
        agent_data = agent.model_dump()
        agent_data.update(updates)
        from datetime import datetime
        agent_data["updated_at"] = datetime.utcnow().isoformat()
        self.agents[agent_id] = Agent(**agent_data)
        self._save()
        return self.agents[agent_id]

    def delete_agent(self, agent_id: str) -> bool:
        if agent_id in self.agents:
            del self.agents[agent_id]
            self._save()
            return True
        return False

    # Workflows
    def create_workflow(self, workflow: Workflow) -> Workflow:
        self.workflows[workflow.id] = workflow
        self._save()
        return workflow

    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        return self.workflows.get(workflow_id)

    def list_workflows(self) -> list[Workflow]:
        return list(self.workflows.values())

    def update_workflow(self, workflow_id: str, updates: dict) -> Optional[Workflow]:
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return None
        wf_data = workflow.model_dump()
        wf_data.update(updates)
        from datetime import datetime
        wf_data["updated_at"] = datetime.utcnow().isoformat()
        self.workflows[workflow_id] = Workflow(**wf_data)
        self._save()
        return self.workflows[workflow_id]

    # Conversations
    def save_conversation(self, conversation_id: str, messages: list[dict]):
        self.conversations[conversation_id] = messages
        self._save()

    def get_conversation(self, conversation_id: str) -> list[dict]:
        return self.conversations.get(conversation_id, [])

    # Users
    def create_user(self, user: User) -> User:
        self.users[user.id] = user
        self._save()
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.email == email:
                return user
        return None


db = Database()
