import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "Seed Agents"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Autonomous Agent SaaS - Personalized AI Assistants"

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Database (SQLite for MVP)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./seed_agents.db")

    # Telegram
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_WEBHOOK_URL: str = os.getenv("TELEGRAM_WEBHOOK_URL", "")

    # AI Service
    AI_API_URL: str = os.getenv("AI_API_URL", "http://localhost:8001/v1/chat/completions")
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "gpt-5")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "seed-agents-secret-key-change-in-production")
    API_KEY_PREFIX: str = "sk-seed-"


settings = Settings()
