from typing import Annotated

from fastapi import Depends

from config.tdp_config import TdpConfig


tdp_config: TdpConfig = TdpConfig()


def get_config() -> TdpConfig:
    return tdp_config


ConfigDep = Annotated[TdpConfig, Depends(get_config)]
