from dataclasses import dataclass


@dataclass(frozen=True)
class SessionMetadata:
    id: str
    start_time: float
