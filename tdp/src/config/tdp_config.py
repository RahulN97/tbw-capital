from typing import Any, Dict

import yaml
from core.config.app_config import AppConfig


class TdpConfig(AppConfig):

    def __init__(self) -> None:
        super().__init__()
        self.service_port: int = int(self.extract_env_var("SERVICE_PORT"))
        self.num_workers: int = int(self.extract_env_var("NUM_WORKERS"))

    def get_log_config(self) -> Dict[str, Any]:
        with open("config/logging.yaml", "r") as f:
            log_config: Dict[str, Any] = yaml.safe_load(f)

        log_level: str = self.log_level.upper()
        for logger in ("", "uvicorn.access", "uvicorn.error"):
            log_config["loggers"][logger]["level"] = log_level

        return log_config
