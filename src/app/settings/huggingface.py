from .base import EnvSettings, Field


class MistralSettings(EnvSettings):
    endpoint: str = Field(alias="HF_MISTRAL_ENDPOINT", default="")
    max_new_tokens: int = Field(alias="HF_MISTRAL_MAX_NEW_TOKENS", default=512)


class HfSettings(EnvSettings):
    token: str = Field(alias="HF_TOKEN", default="")
    mistral: MistralSettings = MistralSettings()
