from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ag-tregistry"
    api_prefix: str = "/api"
    database_url: str = "sqlite:///./ag_tregistry.db"
    agent_architecture_root: Path = Path("tstack/agent-architecture")
    agent_install_root: Path = Path("tstack/.agent")

    model_config = SettingsConfigDict(env_prefix="AG_TREGISTRY_", env_file=".env", extra="ignore")


settings = Settings()
