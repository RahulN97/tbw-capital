from core.config.app_config import AppConfig
from core.logger import logger


class AutotraderConfig(AppConfig):

    def __init__(self) -> None:
        super().__init__()

        self.autotrader_start_delay: float = float(self.extract_env_var("AUTOTRADER_START_DELAY"))
        self.autotrader_wait: float = float(self.extract_env_var("AUTOTRADER_WAIT"))
        self.humanize: bool = self.to_bool(self.extract_env_var("HUMANIZE"))
        self.gds_host: str = self.extract_env_var("GDS_HOST")
        self.gds_port: int = int(self.extract_env_var("GDS_PORT"))

        logger.set_level(self.log_level)
