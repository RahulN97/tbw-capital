from abc import ABC, abstractmethod
from typing import Any


class BaseClient(ABC):

    def __init__(self, client: Any) -> None:
        self.client: Any = client

    @abstractmethod
    def establish_connection(self) -> None:
        pass

    def __getattr__(self, name: str) -> Any:
        return getattr(self.client, name)
