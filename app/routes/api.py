"""
Public API Routes - OpenAI-compatible API for agent interaction.
External clients use these endpoints to interact with their personalized agents.
"""
import uuid
from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import StreamingResponse
from typing import Optional
import json

from app.models.agent import AgentMessage, AgentChatRequest
from app.services.database import db
from app.services.ai_service import chat_with_agent

router = APIRouter(prefix="/v1", tags=["public-api"])


def get_agent_from_key(authorization: str) -> "Agent":
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    api_key = authorization.replace("Bearer ", "").strip()
    agent = db.get_agent_by_api_key(api_key)
    if not agent:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if agent.status.value != "active":
        raise HTTPException(status_code=403, detail="Agent is not active")

    return agent


@router.get("/agents/models")
async def list_agent_models():
    agents = db.list_agents()
    models = []
    for agent in agents:
        if agent.status.value == "active":
            models.append({
                "id": agent.id,
                "object": "model",
                "created": 0,
                "owned_by": "seed-agents",
                "name": agent.name,
                "description": agent.description,
            })
    return {"object": "list", "data": models}


@router.post("/agents/chat/completions")
async def agent_chat_completions(
    request: AgentChatRequest,
    authorization: Optional[str] = Header(None),
):
    agent = None

    if authorization:
        agent = get_agent_from_key(authorization)
    else:
        agent = db.get_agent(request.agent_id)

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    conversation_id = str(uuid.uuid4())

    # Save conversation
    conv_key = f"api_{agent.id}_{conversation_id}"
    messages_dicts = [m.model_dump() for m in request.messages]

    if request.stream:
        async def stream_generator():
            response_gen = await chat_with_agent(agent, request.messages, stream=True)
            full_response = ""
            async for chunk in response_gen:
                if chunk == "[DONE]":
                    yield f"data: [DONE]\n\n"
                    break
                full_response += chunk
                data = {
                    "id": f"chatcmpl-{conversation_id[:8]}",
                    "object": "chat.completion.chunk",
                    "choices": [{
                        "index": 0,
                        "delta": {"content": chunk},
                        "finish_reason": None,
                    }],
                }
                yield f"data: {json.dumps(data)}\n\n"

            messages_dicts.append({"role": "assistant", "content": full_response})
            db.save_conversation(conv_key, messages_dicts)
            db.update_agent(agent.id, {
                "total_messages": agent.total_messages + len(request.messages) + 1,
                "total_conversations": agent.total_conversations + 1,
            })

        return StreamingResponse(
            stream_generator(),
            media_type="text/event-stream",
        )

    result = await chat_with_agent(agent, request.messages, stream=False)

    messages_dicts.append({"role": "assistant", "content": result["content"]})
    db.save_conversation(conv_key, messages_dicts)
    db.update_agent(agent.id, {
        "total_messages": agent.total_messages + len(request.messages) + 1,
        "total_conversations": agent.total_conversations + 1,
    })

    return {
        "id": f"chatcmpl-{conversation_id[:8]}",
        "object": "chat.completion",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": result["content"],
            },
            "finish_reason": "stop",
        }],
        "usage": result.get("usage", {}),
        "agent_id": agent.id,
        "conversation_id": conversation_id,
    }
