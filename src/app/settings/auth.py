from .base import EnvSettings, Field


class JwtSettings(EnvSettings):
    scheme: str = Field(alias="JWT_SCHEME", default="Token")
    algorithms: list[str] = Field(alias="JWT_ALGORITHMS", default=["RS256"])
