from dotenv import dotenv_values
from pathlib import Path

USER_NAME = "Panda"
BOT_NAME = "Ligo"

BASE_DIR = Path(__file__).resolve().parents[1]
env_vars = dotenv_values(BASE_DIR / ".env")
GEMINI_API_KEY = env_vars.get("GEMINI_API_KEY")
OPENROUTER_API_KEY = env_vars.get("OPENROUTER_API_KEY")

# providers = ["gemini", "openrouter"]
