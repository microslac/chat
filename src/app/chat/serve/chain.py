from typing import Any, Dict, TypedDict
from fastapi import Request
from langchain_core.runnables import Runnable
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.schema.runnable.utils import ConfigurableFieldSpec

from app.chat.serve.memory import CustomSQLChatMessageHistory


async def per_req_config_modifier(
    config: Dict[str, Any], request: Request
) -> Dict[str, Any]:
    config = config.copy()
    configurable = config.get("configurable", {})
    config.update(configurable=configurable)
    return config


def create_chain(chain: Runnable, memory: int = 10):
    assert memory % 2 == 0

    def get_chat_history(bot: str, user: str, chat: str) -> CustomSQLChatMessageHistory:
        history = CustomSQLChatMessageHistory(
            bot_id=bot, user_id=user, chat_id=chat, memory=memory
        )
        return history

    history_chain = RunnableWithMessageHistory(
        chain,
        get_chat_history,
        input_messages_key="input",
        history_messages_key="history",
        history_factory_config=[
            ConfigurableFieldSpec(
                id="bot", annotation=str, is_shared=True, default="B0123456789"
            ),
            ConfigurableFieldSpec(
                id="user", annotation=str, is_shared=True, default="U0123456789"
            ),
            ConfigurableFieldSpec(
                id="chat", annotation=str, is_shared=True, default="C0123456789"
            ),
        ],
    ).with_types(input_type=TypedDict("InputChat", {"input": str}))

    return history_chain
