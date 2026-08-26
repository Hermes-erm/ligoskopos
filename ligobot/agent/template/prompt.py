# Make it work first, structure it later
from pathlib import Path


def load_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


WORKSPACE_DIR = Path(__file__).resolve().parent / "workspace"

soul = load_file(WORKSPACE_DIR / "SOUL.md")
agent = load_file(WORKSPACE_DIR / "AGENTS.md")

print(soul)
print("*" * 70)
print(agent)
