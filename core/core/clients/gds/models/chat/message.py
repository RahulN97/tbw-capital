from dataclasses import dataclass


@dataclass
class Message:
    content: str
    sender: str
    time: float
