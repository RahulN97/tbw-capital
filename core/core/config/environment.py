from enum import Enum, auto


class Environment(Enum):

    NOT_SPECIFIED = auto()
    DEV = auto()
    PROD = auto()

    @classmethod
    def from_str(cls, env: str) -> "Environment":
        env: str = env.lower()
        if env == "dev":
            return cls.DEV
        if env == "prod":
            return cls.PROD
        return cls.NOT_SPECIFIED
