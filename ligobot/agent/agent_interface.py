import json
from typing import Literal
from agent.tools.registry import tool_defs, tool_functions
from agent.llm_client import LLMClient
from .context_builder import ContextBuilder
from .contracts import ChatResponse, Base, History
from config import BOT_NAME, LOOP_DEPTH, console, engine
from rich.panel import Panel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func


class Agent:
    """
    Coordinates the agent's core execution flow.

        1. Build the context for the LLM.
        2. Send prompts to the configured LLM client.
        3. Manage conversation and long-term memory.
            1. MEMORY.md
            2. SOUL.md
            3. USER.md
        4. Execute tools requested by the LLM.
        5. Maintain conversation history.
    """

    status = console.status("Agent executing")

    def __init__(self, llm_client: LLMClient, context_builder: ContextBuilder):
        self.llm_client = llm_client
        self.context_builder = context_builder
        self.tools = tool_defs

        Session = sessionmaker(bind=engine)
        Base.metadata.create_all(bind=engine)

        self.session = Session()

    def _process_stream_data(self, chunk):
        print(chunk, end="", flush=True)

    def run(self, user_prompt: str):
        self.status.start()

        result = self._loop(user_prompt)

        if result is not None:
            self._log_response(result)

        self.status.stop()

    def _loop(self, user_req):
        loop_cnt = 1

        response = self.llm_client.generate(
            self.context_builder.system_prompt, user_req
        )

        self._save_conv(role="user", message=user_req, type="text")  # null on user

        while True:

            if loop_cnt >= LOOP_DEPTH:
                self._log_error("Maximum loop depth exceeded")
                return None

            self._status_update(f"{BOT_NAME} thinking..")

            # print(response)

            if response.response_type == "tool_call":
                fn_name = response.tool_call.function_name
                fn_args = response.tool_call.function_arguments

                self._status_update(f"Executing tool '{fn_name}()'", "tool")

                fn_result = tool_functions[fn_name](**fn_args)

                self._save_conv(
                    role="llm",
                    message=f"Tool result: {fn_result}",
                    type=response.response_type,
                )

                response = self.llm_client.generate(
                    self.context_builder.system_prompt
                    + f"\nLast function call result: {fn_result}",
                    user_req,
                )
            elif response.response_type == "error":
                self._log_error(response.error.message)
                break
            else:
                self._save_conv(
                    role="llm",
                    message=response.text_output,
                    type=response.response_type,
                )
                return response.text_output

            loop_cnt += 1

    def _log_response(self, response):
        console.print(
            Panel(
                response,
                title="[bold cyan]Ligo[/bold cyan]",
                border_style="cyan",
                padding=(0, 1),
            )
        )

    def _status_update(
        self,
        desc: str,
        status_type: Literal["info", "progress", "tool", "success", "error"] = "info",
        spinner: str | None = None,
    ):

        styles = {
            "info": "[cyan]",
            "progress": "[yellow]",
            "tool": "[blue]",
            "success": "[green]",
            "error": "[red]",
        }

        self.status.update(
            status=f"{styles[status_type]}{desc}",
            spinner=spinner,
        )

    def _log_error(self, err_msg):
        console.print(
            f"[bold red]\nERROR:[/] {err_msg}, Try again",
            style="yellow",
        )

    def _get_chats(self, conv_limit: int):
        max_id = self.session.query(func.max(History.conversation_id)).scalar()

        result = (
            self.session.query(History)
            .where(History.conversation_id > max_id - conv_limit)
            .order_by(History.created_at)
            .all()
        )

        return result

    def _save_conv(
        self,
        role: Literal["user", "llm"],
        message: str,
        type: Literal["text", "tool_call"],
    ):
        last_conv_id = (
            self.session.query(History.conversation_id)
            .order_by(History.created_at.desc())
            .limit(1)
            .scalar()
        )

        last_conv_id = last_conv_id if role == "llm" else (last_conv_id or 0) + 1

        data = History(
            role=role, message=message, response_type=type, conversation_id=last_conv_id
        )
        self.session.add(data)
        self.session.commit()


# run(): self.llm_client.provider.stream_chat(user_prompt, self._process_stream_data)
