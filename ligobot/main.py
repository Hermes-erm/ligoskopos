from config import USER_NAME, BOT_NAME
from agent import Agent, LLMClient, Gemini, OpenRouter, Groq, ContextBuilder
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML


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


# print("Ligo waking up..")
if __name__ == "__main__":

    # llm_provider = OpenRouter(model="nvidia/nemotron-3.5-lightning:free")
    # llm_provider = Gemini(model="gemini-3.5-flash-lite")
    llm_provider = Groq(model="qwen/qwen3.6-27b")

    agent = Agent(
        llm_client=LLMClient(llm_provider), context_builder=ContextBuilder()
    )  # vary on session (implement it on later)

    start(agent)
