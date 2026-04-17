from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    postgres_db: str = Field(validation_alias=AliasChoices("DB_NAME"))
    postgres_user: str = Field(validation_alias=AliasChoices("DB_USER"))
    postgres_password: str = Field(validation_alias=AliasChoices("DB_PASSWORD"))
    postgres_host: str = Field(
        default="postgres", validation_alias=AliasChoices("DB_HOST")
    )
    postgres_port: int = Field(validation_alias=AliasChoices("DB_PORT"))

    es_host: str = Field(
        validation_alias=AliasChoices("ES_HOST"),
    )
    es_index: str = Field(validation_alias=AliasChoices("ES_INDEX"))

    state_file: str = "/state/etl_state.json"
    batch_size: int = 500
    poll_interval_sec: int = 5
    backoff_initial_sec: float = 1.0
    backoff_max_sec: float = 60.0
    backoff_jitter_sec: float = 0.5

    @property
    def pg_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
