from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class RabbitMQSettings(BaseModel):
    host: str
    port: int
    login: str
    password: str
    pika_consumer_queue_name: str


class PostgresSettings(BaseModel):
    host: str
    port: int
    user: str
    password: str
    db: str
    pool_size: int

    def get_dsn(self, db: str) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{db}"

    def get_external_dsn(self, db: str) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@localhost:7432/{db}"


class Settings(BaseSettings):
    debug: bool = False

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        extra="ignore",
    )

    environment: str = "local"
    log_level: str = "INFO"

    jwt_algorithm: str
    secret_key: str
    thread_pool_workers: int
    cors_origins: str = ""
    base_url: str = "http://localhost:8001"

    rabbit: RabbitMQSettings
    postgres: PostgresSettings


settings = Settings()
