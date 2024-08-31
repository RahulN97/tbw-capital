from dataclasses import dataclass


@dataclass(frozen=True)
class ItemMetadata:
    id: int
    name: str
    limit: int
    members: bool
