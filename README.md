# Ligoskopos

> A minimal, extensible agentic AI framework built from scratch in Python.

Ligoskopos is an experimental AI agent designed to explore the fundamentals of **agentic systems** without hiding the architecture behind a large framework.

## Setup

### Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- An API key from your chosen LLM provider

### Installation

```bash
git clone https://github.com/Hermes-erm/ligoskopos.git

cd ligoskopos

uv sync
```

### Environment Variables

```bash
cp .env.example .env
```

Add one API key to `.env`. Groq is preferred:

```env
GEMINI_API_KEY=your_key
OPENROUTER_API_KEY=your_key
GROQ_API_KEY=your_key
```

### Run

From the project root:

```bash
uv run ligobot/main.py
```
