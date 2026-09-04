from config import console, USER_NAME, BOT_NAME
from agent import Agent, LLMClient, Gemini, OpenRouter, Groq, ContextBuilder
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from rich.panel import Panel


def start(agent: Agent):
    """
    Run the interactive CLI session.

    Flow:
        1. Receive user input
        2. Build context
        3. Send context to the LLM
        4. Display the response
        5. Repeat until the session ends
    """

    console.print(
        Panel.fit(
            f"[bold cyan]{BOT_NAME}[/bold cyan]\n[dim]Your lightweight AI agent[/dim]",
            border_style="cyan",
        )
    )
    try:
        while True:
            user_prompt = prompt(
                HTML(
                    f"<ansigreen><b>{USER_NAME}</b></ansigreen> <ansidarkcyan>›</ansidarkcyan> "
                ),
                placeholder=HTML(
                    '<style color="#666666"><i>What’s on your mind?</i></style>'
                ),
            )
            user_prompt = user_prompt.strip()

            if not user_prompt:
                continue

            if user_prompt.lower() in ["quit", "bye", "exit", "clear"]:
                console.print("[dim]Catch you later! 👋 Bye[/dim]")
                break

            # Step: Progress of agent running...

            agent.run(user_prompt)

    except KeyboardInterrupt:
        console.print("[dim]\nExiting...[/dim]")


# print("Ligo waking up..")
if __name__ == "__main__":

    # llm_provider = OpenRouter(model="nvidia/nemotron-3.5-lightning:free")
    # llm_provider = Gemini(model="gemini-3.5-flash-lite")
    llm_provider = Groq(model="qwen/qwen3.6-27b")  # Pass None on later

    agent = Agent(llm_client=LLMClient(llm_provider), context_builder=ContextBuilder())
    # vary on session (implement it on later)

    start(agent)
