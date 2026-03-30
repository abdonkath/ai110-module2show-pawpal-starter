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


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        return self.tasks

@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_pets(self) -> List[Pet]:
        return self.pets


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def _get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from all of the owner's pets."""
        all_tasks = []
        for pet in self.owner.get_pets():
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def generate_plan(self) -> List[Task]:
        """Return incomplete tasks sorted by priority (highest first),
        filtered to fit within the owner's available time."""
        pending = [t for t in self._get_all_tasks() if not t.completed]
        pending.sort(key=lambda t: t.priority, reverse=True)

        plan = []
        time_used = 0
        for task in pending:
            if time_used + task.duration_minutes <= self.owner.available_minutes:
                plan.append(task)
                time_used += task.duration_minutes
        return plan

    def explain_plan(self) -> str:
        """Return a human-readable summary of the generated plan."""
        plan = self.generate_plan()
        if not plan:
            return "No tasks fit within the available time."

        lines = [f"Plan for {self.owner.name} ({self.owner.available_minutes} min available):\n"]
        for i, task in enumerate(plan, 1):
            priority_label = "HIGH" if task.is_high_priority() else "normal"
            lines.append(
                f"  {i}. [{priority_label}] {task.name} "
                f"({task.category}, {task.duration_minutes} min)"
            )
        lines.append(f"\nTotal time: {self.get_total_duration()} min")
        return "\n".join(lines)

    def get_total_duration(self) -> int:
        """Return the total minutes of all tasks in the generated plan."""
        return sum(t.duration_minutes for t in self.generate_plan())
