from langchain.llms.huggingface_endpoint import HuggingFaceEndpoint
from transformers import AutoTokenizer

from app.settings import settings
from app.chat.llms.base import create_prompt, create_parser

llm = HuggingFaceEndpoint(
    endpoint_url=settings.hf.llama.endpoint,
    max_new_tokens=settings.hf.llama.max_new_tokens,
    huggingfacehub_api_token=settings.hf.token,
    top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.01,
    repetition_penalty=1.03,
    stop_sequences=["<|start_header_id|>"],
)

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")

prompt = create_prompt(
    tokenizer, start_seq=r"<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
)

parser = create_parser(stop_seq=r"<|eot_id|>")

chain = prompt | llm | parser
