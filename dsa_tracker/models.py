from dataclasses import dataclass
from typing import Optional


@dataclass
class Problem:
    id: Optional[int]
    title: str
    topic: str
    difficulty: str
    platform: str
    status: str
    date_solved: Optional[str] = None
    revision_count: int = 0
    next_revision: Optional[str] = None