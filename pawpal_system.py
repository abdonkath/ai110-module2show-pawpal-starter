from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    name: str
    category: str
    duration_minutes: int
    priority: int
    completed: bool = False
    time: str = "00:00"          # scheduled time in "HH:MM" format
    recurring: bool = False      # whether the task repeats
    interval_days: int = 1       # how often it recurs (in days)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def is_high_priority(self) -> bool:
        """Return True if the task's priority is 4 or higher."""
        return self.priority >= 4


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks

@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def get_pets(self) -> List[Pet]:
        """Return all pets belonging to this owner."""
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

    def sort_by_time(self) -> List[Task]:
        """Return all tasks sorted chronologically by their 'HH:MM' time attribute."""
        return sorted(self._get_all_tasks(), key=lambda t: t.time)

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> List[Task]:
        """Return tasks filtered by pet name and/or completion status.

        Args:
            pet_name: If provided, only tasks belonging to this pet are returned.
            completed: If provided, only tasks matching this completion state are returned.
        """
        results = []
        for pet in self.owner.get_pets():
            if pet_name is not None and pet.name.lower() != pet_name.lower():
                continue
            for task in pet.get_tasks():
                if completed is not None and task.completed != completed:
                    continue
                results.append(task)
        return results

    def get_recurring_tasks(self) -> List[Task]:
        """Return all tasks marked as recurring across all pets."""
        return [t for t in self._get_all_tasks() if t.recurring]

    def detect_conflicts(self) -> List[tuple]:
        """Return pairs of tasks scheduled at the same time (conflict detection).

        Uses a simple O(n²) scan comparing 'HH:MM' time strings. Returns a list
        of (task_a, task_b) tuples where both tasks share the same time slot.
        """
        tasks = [t for t in self._get_all_tasks() if t.time != "00:00"]
        conflicts = []
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                if tasks[i].time == tasks[j].time:
                    conflicts.append((tasks[i], tasks[j]))
        return conflicts
