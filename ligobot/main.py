from config import USER_NAME, BOT_NAME
from agent.agent_interface import Agent
from agent.llm_client import LLMClient, Gemini, OpenAI
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML


def start(agent: Agent):
    """
    CLI session loop.

    Flow:
        1. Receive user input
        2. Assemble context
        3. Send context to LLM
        4. Display response
    """

    print(f"{BOT_NAME}: Hello {USER_NAME}")
    try:
        while True:
            user_prompt = prompt(
                f"{USER_NAME}: ",
                placeholder=HTML(
                    '<i><style color="#888888"> whats on your mind..</style></i>'
                ),
            )
            user_prompt = user_prompt.strip()

            if not user_prompt:
                continue

            if user_prompt.lower() in ["quit", "bye", "exit"]:
                print(f"{BOT_NAME}: Catch you later! 👋 Bye")
                break

            # Step: Progress of agent running...

            agent.run(user_prompt)

    except KeyboardInterrupt:
        print(f"\n{BOT_NAME}: Exiting...")


if __name__ == "__main__":
    # print("Ligo waking up..")
    llm_provider = Gemini(model="gemini-3.5-flash-lite")
    agent = Agent(LLMClient(llm_provider))  # vary on session (implement it on later)
    start(agent)
