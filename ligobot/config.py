from dotenv import dotenv_values
from pathlib import Path
from rich.console import Console
from sqlalchemy import create_engine

console = Console()

USER_NAME = "Hermes"
BOT_NAME = "Ligo"

BASE_DIR = Path(__file__).resolve().parents[1]
env_vars = dotenv_values(BASE_DIR / ".env")
GEMINI_API_KEY = env_vars.get("GEMINI_API_KEY")
OPENROUTER_API_KEY = env_vars.get("OPENROUTER_API_KEY")
GROQ_API_KEY = env_vars.get("GROQ_API_KEY")

LOOP_DEPTH = 10

DATABASE_URL = f"sqlite:///{BASE_DIR / "history.db"}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,  # True on terminal logs
)
