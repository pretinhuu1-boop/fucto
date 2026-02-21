"""
Seed Agents - Run both the original OpenAI API server and the Seed Agents platform.
"""
import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("=" * 50)
    print("  SEED AGENTS - Autonomous Agent SaaS")
    print("=" * 50)
    print(f"  Dashboard: http://localhost:{settings.PORT}")
    print(f"  API Docs:  http://localhost:{settings.PORT}/docs")
    print(f"  Health:    http://localhost:{settings.PORT}/health")
    print("=" * 50)
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )
