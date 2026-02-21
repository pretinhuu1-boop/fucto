"""
Telegram Routes - Webhook and bot management endpoints.
"""
from fastapi import APIRouter, HTTPException, Request

from app.config import settings
from app.services.telegram_bot import (
    handle_telegram_update,
    set_webhook,
    remove_webhook,
    send_message,
)
from app.services.database import db

router = APIRouter(prefix="/api/telegram", tags=["telegram"])


@router.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
        result = await handle_telegram_update(update)
        return {"ok": True, "result": result}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@router.post("/setup")
async def setup_webhook(webhook_url: str = ""):
    if not settings.TELEGRAM_BOT_TOKEN:
        raise HTTPException(status_code=400, detail="TELEGRAM_BOT_TOKEN not configured")

    url = webhook_url or settings.TELEGRAM_WEBHOOK_URL
    if not url:
        raise HTTPException(status_code=400, detail="No webhook URL provided")

    result = await set_webhook(url)
    return {"message": "Webhook configured", "result": result}


@router.post("/remove-webhook")
async def remove_webhook_endpoint():
    result = await remove_webhook()
    return {"message": "Webhook removed", "result": result}


@router.post("/send")
async def send_direct_message(chat_id: str, text: str):
    result = await send_message(chat_id, text)
    return result


@router.get("/status")
async def telegram_status():
    linked_agents = [
        {"id": a.id, "name": a.name, "chat_id": a.telegram_chat_id}
        for a in db.agents.values()
        if a.telegram_linked
    ]
    return {
        "bot_configured": bool(settings.TELEGRAM_BOT_TOKEN),
        "webhook_url": settings.TELEGRAM_WEBHOOK_URL,
        "linked_agents": linked_agents,
        "total_linked": len(linked_agents),
    }
