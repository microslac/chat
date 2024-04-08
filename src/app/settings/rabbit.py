from .base import EnvSettings, Field


class RabbitSettings(EnvSettings):
    protocol: str = Field(alias="RABBITMQ_PROTOCOL", default="amqp")
    host: str = Field(alias="RABBITMQ_HOST", default="localhost")
    port: int = Field(alias="RABBITMQ_PORT", default=5672)
    username: str = Field(alias="RABBITMQ_USERNAME", default="")
    password: str = Field(alias="RABBITMQ_PASSWORD", default="")

    @property
    def url(self):
        return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}/"
