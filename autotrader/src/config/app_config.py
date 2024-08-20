import os
from typing import Optional

from config.exceptions import MissingConfigError
from utils.logging import DEFAULT_LOG_LEVEL, logger


class AppConfig:

    def __init__(self) -> None:
        self.f2p: bool = self._to_bool(self._extract_env_var("F2P"))
        self.autotrader_start_delay: float = float(self._extract_env_var("AUTOTRADER_START_DELAY"))
        self.autotrader_wait: float = float(self._extract_env_var("AUTOTRADER_WAIT"))
        self.humanize: bool = self._to_bool(self._extract_env_var("HUMANIZE"))
        self.gds_host: str = self._extract_env_var("GDS_HOST")
        self.gds_port: int = int(self._extract_env_var("GDS_PORT"))

        self._set_log_level()

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

    def _set_log_level(self) -> None:
        if (log_level := os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL)) != DEFAULT_LOG_LEVEL:
            logger.setLevel(log_level.upper())
