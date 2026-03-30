from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    task = Task(name="Morning Walk", category="Exercise", duration_minutes=30, priority=5)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(name="Bath Time", category="Grooming", duration_minutes=20, priority=3))
    assert len(pet.get_tasks()) == 1
