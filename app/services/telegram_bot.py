"""
Telegram Bot Service - Connects agents to Telegram for delivery.
Each agent can be linked to a Telegram chat for direct interaction.
"""
import httpx
import json
from typing import Optional

from app.config import settings
from app.models.agent import Agent, AgentMessage
from app.services.database import db
from app.services.ai_service import chat_with_agent


TELEGRAM_API = "https://api.telegram.org/bot{token}"


def get_api_url(method: str) -> str:
    return f"{TELEGRAM_API.format(token=settings.TELEGRAM_BOT_TOKEN)}/{method}"


async def set_webhook(webhook_url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            get_api_url("setWebhook"),
            json={"url": webhook_url},
        )
        return response.json()


async def remove_webhook() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            get_api_url("deleteWebhook"),
        )
        return response.json()


async def send_message(chat_id: str, text: str, parse_mode: str = "Markdown") -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            get_api_url("sendMessage"),
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode,
            },
        )
        return response.json()


async def send_typing_action(chat_id: str) -> None:
    async with httpx.AsyncClient() as client:
        await client.post(
            get_api_url("sendChatAction"),
            json={"chat_id": chat_id, "action": "typing"},
        )


def find_agent_for_chat(chat_id: str) -> Optional[Agent]:
    for agent in db.agents.values():
        if agent.telegram_linked and agent.telegram_chat_id == str(chat_id):
            return agent
    return None


async def handle_telegram_update(update: dict) -> Optional[str]:
    message = update.get("message")
    if not message:
        return None

    chat_id = str(message["chat"]["id"])
    text = message.get("text", "")
    user_name = message.get("from", {}).get("first_name", "User")

    if text == "/start":
        welcome = (
            f"Ola {user_name}! Bem-vindo ao *Seed Agents*.\n\n"
            "Sou um assistente inteligente pronto para ajudar.\n\n"
            "Comandos:\n"
            "/start - Inicio\n"
            "/agents - Ver agentes disponiveis\n"
            "/link <agent_id> - Conectar a um agente\n"
            "/status - Ver status atual\n\n"
            "Envie qualquer mensagem para conversar!"
        )
        await send_message(chat_id, welcome)
        return "welcome_sent"

    if text == "/agents":
        agents = db.list_agents()
        if not agents:
            await send_message(chat_id, "Nenhum agente disponivel no momento.")
            return "no_agents"
        agent_list = "\n".join(
            f"- `{a.id[:8]}` | *{a.name}* - {a.description[:60]}"
            for a in agents
            if a.status.value == "active"
        )
        await send_message(
            chat_id,
            f"*Agentes Disponiveis:*\n\n{agent_list}\n\nUse /link <id> para conectar.",
        )
        return "agents_listed"

    if text.startswith("/link "):
        agent_id_prefix = text[6:].strip()
        matched = None
        for agent in db.agents.values():
            if agent.id.startswith(agent_id_prefix):
                matched = agent
                break
        if matched:
            db.update_agent(matched.id, {
                "telegram_linked": True,
                "telegram_chat_id": chat_id,
            })
            await send_message(
                chat_id,
                f"Conectado ao agente *{matched.name}*!\n"
                f"Agora suas mensagens serao respondidas por este agente.",
            )
            return "agent_linked"
        else:
            await send_message(chat_id, "Agente nao encontrado. Use /agents para ver disponiveis.")
            return "agent_not_found"

    if text == "/status":
        agent = find_agent_for_chat(chat_id)
        if agent:
            await send_message(
                chat_id,
                f"*Agente Conectado:* {agent.name}\n"
                f"*Tipo:* {agent.agent_type.value}\n"
                f"*Status:* {agent.status.value}\n"
                f"*Conversas:* {agent.total_conversations}\n"
                f"*Mensagens:* {agent.total_messages}",
            )
        else:
            await send_message(
                chat_id,
                "Nenhum agente conectado. Use /link <id> para conectar.",
            )
        return "status_sent"

    # Regular message - route to linked agent
    agent = find_agent_for_chat(chat_id)
    if not agent:
        # Use first active agent as default
        active_agents = [a for a in db.agents.values() if a.status.value == "active"]
        if active_agents:
            agent = active_agents[0]
            db.update_agent(agent.id, {
                "telegram_linked": True,
                "telegram_chat_id": chat_id,
            })
        else:
            await send_message(
                chat_id,
                "Nenhum agente ativo. Crie um agente primeiro no painel do Seed Agents.",
            )
            return "no_active_agent"

    await send_typing_action(chat_id)

    # Get conversation history
    conv_key = f"tg_{chat_id}_{agent.id}"
    history = db.get_conversation(conv_key)
    history.append({"role": "user", "content": text})

    messages = [AgentMessage(role=m["role"], content=m["content"]) for m in history[-20:]]

    result = await chat_with_agent(agent, messages, stream=False)
    response_text = result["content"]

    history.append({"role": "assistant", "content": response_text})
    db.save_conversation(conv_key, history[-50:])

    # Update stats
    db.update_agent(agent.id, {
        "total_messages": agent.total_messages + 2,
    })

    await send_message(chat_id, response_text, parse_mode="Markdown")
    return "message_handled"
