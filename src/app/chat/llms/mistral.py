from langchain.llms.huggingface_endpoint import HuggingFaceEndpoint
from transformers import AutoTokenizer

from app.settings import settings
from app.chat.llms.base import create_prompt, create_parser

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

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

prompt = create_prompt(tokenizer, start_seq=r"   ")

parser = create_parser(stop_seq=r"</s>")

chain = prompt | llm | parser
