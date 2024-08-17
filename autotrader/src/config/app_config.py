import os
from typing import Optional

from config.exceptions import MissingConfigError


class AppConfig:

    def __init__(self) -> None:
        self.humanize: bool = self._to_bool(self._extract_env_var("HUMANIZE"))
        self.price_url: str = self._extract_env_var("PRICE_URL")
        self.gds_host: str = self._extract_env_var("GDS_HOST")
        self.gds_port: int = int(self._extract_env_var("GDS_PORT"))

    @staticmethod
    def _raise_if_missing(val: Optional[str], var_name: str) -> str:
        if val is None:
            raise MissingConfigError(var_name)
        return val

    @staticmethod
    def _to_bool(val: str) -> bool:
        return val.lower() in ("true", "1")

    def _extract_env_var(self, var_name: str) -> str:
        return self._raise_if_missing(os.getenv(var_name), var_name)
