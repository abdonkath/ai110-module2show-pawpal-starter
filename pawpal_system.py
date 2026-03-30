from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    name: str
    category: str
    duration_minutes: int
    priority: int
    completed: bool = False

    def mark_complete(self) -> None:
        self.completed = True

    def is_high_priority(self) -> bool:
        return self.priority >= 4
