# configure environment variables to be parsed into an AppConfig
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from .secrets import secrets_manager
import logging
from typing import cast

logger = logging.getLogger(__name__)


class GoogleConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    client_id: str = Field(default="")
    client_secret: str = Field(default="")
    scopes: str = (
        "email profile openid https://www.googleapis.com/auth/gmail.modify https://www.googleapis.com/auth/calendar"
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Use secrets manager for sensitive Google credentials
        _secret_val: int | str | None = secrets_manager.get_secret(
            name="GOOGLE__CLIENT_SECRET", default=self.client_secret
        )
        if not isinstance(_secret_val, str):
            logger.warn(
                f"GOOGLE__CLIENT_SECRET returned non-string value {_secret_val}"
            )
            _secret_val = str(_secret_val)

        self.client_secret = _secret_val


class OpenAIConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    api_key: str = Field(default="")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Use secrets manager for OpenAI API key
        _secret_val: int | str | None = secrets_manager.get_secret(
            name="OPENAI__API_KEY", default=self.api_key
        )

        if not isinstance(_secret_val, str):
            logger.warn(f"OPENAI__API_KEY returned non-string value {_secret_val}")
            _secret_val = str(_secret_val)

        self.api_key = _secret_val


class SupabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    url: str = Field(default="")
    anon_key: str = Field(default="")
    service_role_key: str = Field(default="")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Use secrets manager for sensitive Supabase keys
        _anon_key_secret_val: int | str | None = secrets_manager.get_secret(
            name="SUPABASE__ANON_KEY", default=self.anon_key
        )
        if not isinstance(_anon_key_secret_val, str):
            logger.warn(
                f"SUPABASE__ANON_KEY returned non-string value {_anon_key_secret_val}"
            )
            _anon_key_secret_val = str(_anon_key_secret_val)

        self.anon_key = _anon_key_secret_val

        _service_role_key_secret_val = secrets_manager.get_secret(
            name="SUPABASE__SERVICE_ROLE_KEY", default=self.service_role_key
        )

        if not isinstance(_service_role_key_secret_val, str):
            logger.warn(
                f"SUPABASE__SERVICE_ROLE_KEY returned non-string value {_service_role_key_secret_val}"
            )
            _service_role_key_secret_val = str(_service_role_key_secret_val)

        self.service_role_key = _service_role_key_secret_val


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    username: str = Field(default="")
    password: str = Field(default="")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Use secrets manager for database credentials
        _user_name_secret_val = secrets_manager.get_secret(
            name="DATABASE__USERNAME", default=self.username
        )

        if not isinstance(_user_name_secret_val, str):
            logger.warn(
                f"DATABASE__USERNAME returned non-string value {_user_name_secret_val}"
            )
            _user_name_secret_val = str(_user_name_secret_val)

        self.username = _user_name_secret_val

        _password_secret_val = secrets_manager.get_secret(
            name="DATABASE__PASSWORD", default=self.password
        )

        if not isinstance(_password_secret_val, str):
            logger.warn(
                f"DATABASE__PASSWORD returned non-string value {_password_secret_val}"
            )
            _password_secret_val = str(_password_secret_val)

        self.password = _password_secret_val


class GroqConfig(BaseSettings):
    api_key: str = Field(default="")


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", extra="allow")

    # API Keys
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    groq: GroqConfig = Field(default_factory=GroqConfig)

    # Auth Configuration
    supabase: SupabaseConfig = Field(default_factory=SupabaseConfig)
    google: GoogleConfig = Field(default_factory=GoogleConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    environment: str = Field(default="local")  # local, prod


config = AppConfig()
