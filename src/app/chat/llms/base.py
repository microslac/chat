from typing import Any, AsyncIterator

from transformers import PreTrainedTokenizer
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompt_values import ChatPromptValue, PromptValue
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableGenerator


def create_prompt(tokenizer: PreTrainedTokenizer, start_seq: str = ""):
    class LlamaChatPromptValue(ChatPromptValue):
        def to_string(self) -> str:
            dict_messages = []
            for m in self.messages:
                if isinstance(m, SystemMessage):
                    role = "system"
                elif isinstance(m, HumanMessage):
                    role = "user"
                elif isinstance(m, AIMessage):
                    role = "assistant"
                else:
                    raise ValueError(f"Got unsupported message type: {m}")
                msg = {"role": role, "content": m.content}
                dict_messages.append(msg)
            message = (
                tokenizer.apply_chat_template(dict_messages, tokenize=False) + start_seq
            )
            return message

    class LlamaChatPromptTemplate(ChatPromptTemplate):
        def format_prompt(self, **kwargs: Any) -> PromptValue:
            messages = self.format_messages(**kwargs)
            return LlamaChatPromptValue(messages=messages)

    prompt = LlamaChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )
    return prompt


def create_parser(stop_seq: str = ""):
    async def parse(chunks: AsyncIterator[str]) -> AsyncIterator[str]:
        async for chunk in chunks:
            yield chunk.lstrip()
            break

        async for chunk in chunks:
            yield chunk.replace(stop_seq, "")

    parser = RunnableGenerator(parse)
    return parser
