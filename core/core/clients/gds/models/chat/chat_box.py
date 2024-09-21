from dataclasses import dataclass
from typing import List

from core.clients.gds.models.chat.message import Message


@dataclass
class ChatBox:
    messages: List[Message]
