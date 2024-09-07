from abc import ABC, abstractmethod


class BaseClient(ABC):

    def __init__(self) -> None:
        try:
            self.establish_connection()
        except Exception as e:
            raise ConnectionError(
                f"Unable to establish stable connection to server through client: {self.__class__.__name__}\n"
                f"Details: {str(e)}"
            )

    @abstractmethod
    def establish_connection(self) -> None:
        pass
