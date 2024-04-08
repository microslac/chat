from typing import Any, Dict, TypedDict, AsyncIterator
from fastapi import Request

from langchain.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain.schema.runnable.utils import ConfigurableFieldSpec
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompt_values import PromptValue, ChatPromptValue
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableGenerator
from transformers import AutoTokenizer

from app.settings import settings
from app.chat.llms.memory import CustomSQLChatMessageHistory

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")


def get_chat_history_factory(agent: str):
    def get_chat_history(bot: str, user: str, chat: str) -> CustomSQLChatMessageHistory:
        # TODO: max tokens
        history = CustomSQLChatMessageHistory(
            bot_id=bot, user_id=user, chat_id=chat, last=10
        )
        return history

    return get_chat_history


class MistralChatPromptValue(ChatPromptValue):
    def to_string(self) -> str:
        dict_messages = []
        for m in self.messages:
            if isinstance(m, HumanMessage):
                role = "user"
            elif isinstance(m, AIMessage):
                role = "assistant"
            else:
                raise ValueError(f"Got unsupported message type: {m}")
            msg = {"role": role, "content": m.content}
            dict_messages.append(msg)
        message = tokenizer.apply_chat_template(dict_messages, tokenize=False) + "  "
        return message


class MistralChatPromptTemplate(ChatPromptTemplate):
    def format_prompt(self, **kwargs: Any) -> PromptValue:
        messages = self.format_messages(**kwargs)
        return MistralChatPromptValue(messages=messages)


async def parse(chunks: AsyncIterator[str]) -> AsyncIterator[str]:
    async for chunk in chunks:
        yield chunk.lstrip()
        break

    async for chunk in chunks:
        yield chunk.replace(r"</s>", "")


prompt = MistralChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

llm = HuggingFaceEndpoint(
    endpoint_url=settings.hf.mistral.endpoint,
    max_new_tokens=settings.hf.mistral.max_new_tokens,
    huggingfacehub_api_token=settings.hf.token,
    top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.01,
    repetition_penalty=1.03,
)

parser = RunnableGenerator(parse)

_chain = prompt | llm | parser

chain = RunnableWithMessageHistory(
    _chain,
    get_chat_history_factory("agent"),
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


async def per_req_config_modifier(
    config: Dict[str, Any], request: Request
) -> Dict[str, Any]:
    config = config.copy()
    configurable = config.get("configurable", {})
    config.update(configurable=configurable)

    return config
