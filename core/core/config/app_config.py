import os
from typing import Optional

from core.config.environment import Environment
from core.config.exceptions import MissingConfigError


class AppConfig:

    DEFAULT_LOG_LEVEL: str = "INFO"

    def __init__(self) -> None:
        self.env: Environment = Environment.from_str(self.extract_env_var("ENV"))
        self.log_level: str = os.getenv("LOG_LEVEL", self.DEFAULT_LOG_LEVEL).upper()

    @staticmethod
    def raise_if_missing(val: Optional[str], var_name: str) -> str:
        if val is None:
            raise MissingConfigError(var_name)
        return val

    @staticmethod
    def to_bool(val: str) -> bool:
        return val.lower() in ("true", "1")

    def extract_env_var(self, var_name: str) -> str:
        return self.raise_if_missing(os.getenv(var_name), var_name)
