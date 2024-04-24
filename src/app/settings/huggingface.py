from .base import EnvSettings, Field


class MistralSettings(EnvSettings):
    endpoint: str = Field(alias="HF_MISTRAL_ENDPOINT", default="")
    max_new_tokens: int = Field(alias="HF_MISTRAL_MAX_NEW_TOKENS", default=512)


class LlamaSettings(EnvSettings):
    endpoint: str = Field(alias="HF_LLAMA_ENDPOINT", default="")
    max_new_tokens: int = Field(alias="HF_LLAMA_MAX_NEW_TOKENS", default=512)


class PhiSettings(EnvSettings):
    endpoint: str = Field(alias="HF_PHI_ENDPOINT", default="")
    max_new_tokens: int = Field(alias="HF_PHI_MAX_NEW_TOKENS", default=512)


class HfSettings(EnvSettings):
    token: str = Field(alias="HF_TOKEN", default="")
    mistral: MistralSettings = MistralSettings()
    llama: LlamaSettings = LlamaSettings()
    phi: PhiSettings = PhiSettings()
