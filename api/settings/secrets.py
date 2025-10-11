"""
Secrets management module that handles environment-based secret retrieval.
For production (ENVIRONMENT=prod), secrets are pulled from AWS Secrets Manager.
For other environments, secrets are pulled from environment variables.
"""

import os
import json
import boto3
import logging

logger = logging.getLogger(__name__)

client = boto3.client("secretsmanager")


class SecretsManager:
    """Handles secret retrieval based on environment."""

    def __init__(self) -> None:
        self.secrets_name: str | None = os.getenv("SECRETS_MANAGER_SECRET_NAME")
        self.environment: str = os.getenv("ENVIRONMENT", "local")
        self._secrets_client = client
        self._secrets_dict: dict | None = self._get_secrets_dict()

    def _get_secrets_dict(self) -> dict[str, str] | None:
        if self.environment == "prod":
            response = self._secrets_client.get_secret_value(SecretId=self.secrets_name)
            return (
                json.loads(response["SecretString"]) if response["SecretString"] else {}
            )
        else:
            return None

    def get_secret(
        self, *, name: str, default: str | int | None = None
    ) -> str | int | None:
        """
        Get a secret value based on environment.

        Args:
            name: Name of the secret in AWS Secrets Manager (for prod)
            env_var_name: Name of the environment variable (for dev)
            default: Default value if secret is not found

        Returns:
            Secret value as string
        """
        print(
            f"Getting secret '{name}' from SECRETS_MANAGER_SECRET_NAME: '{self.secrets_name}' with environment '{self.environment}'"
        )
        if self.environment == "prod":
            assert self._secrets_dict is not None, "In production settings, "
            return (
                self._secrets_dict.get(name, default)
                if default is not ...
                else self._secrets_dict[name]
            )
        else:
            return os.getenv(name, default)


secrets_manager = SecretsManager()
