from .auth import JwtSettings
from .base import EnvSettings
from .database import DatabaseSettings
from .general import ApiSettings, CorsSettings, MicroserviceSettings
from .rabbit import RabbitSettings
from .redis import RedisSettings
from .huggingface import HfSettings
from .test import TestSettings

__all__ = ["settings"]


class Settings(EnvSettings):
    api: ApiSettings = ApiSettings()
    cors: CorsSettings = CorsSettings()
    db: DatabaseSettings = DatabaseSettings()
    ms: MicroserviceSettings = MicroserviceSettings()
    rabbit: RabbitSettings = RabbitSettings()
    redis: RedisSettings = RedisSettings()
    test: TestSettings = TestSettings()
    jwt: JwtSettings = JwtSettings()
    hf: HfSettings = HfSettings()


settings = Settings()
