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
        pass

    def is_high_priority(self) -> bool:
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> List[Pet]:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet

    def generate_plan(self) -> List[Task]:
        pass

    def explain_plan(self) -> str:
        pass

    def get_total_duration(self) -> int:
        pass
