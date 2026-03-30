from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# ── helpers ───────────────────────────────────────────────────────────────────

def make_scheduler(*pets):
    """Return a Scheduler with 120 min available and the given pets registered."""
    owner = Owner(name="Alex", available_minutes=120)
    for pet in pets:
        owner.add_pet(pet)
    return Scheduler(owner)


# ── existing tests ────────────────────────────────────────────────────────────

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


# ── sorting ───────────────────────────────────────────────────────────────────

def test_sort_by_time_returns_chronological_order():
    """Tasks added out of order should come back sorted by HH:MM."""
    buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    buddy.add_task(Task(name="Evening Walk",  category="Exercise", duration_minutes=20, priority=3, time="18:00"))
    buddy.add_task(Task(name="Morning Feed",  category="Feeding",  duration_minutes=10, priority=5, time="07:30"))
    buddy.add_task(Task(name="Midday Brush",  category="Grooming", duration_minutes=15, priority=2, time="12:00"))

    scheduler = make_scheduler(buddy)
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]
    assert times == sorted(times)


def test_sort_by_time_single_task():
    """A pet with one task should return that task unchanged."""
    buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    buddy.add_task(Task(name="Only Task", category="Health", duration_minutes=10, priority=3, time="09:00"))
    scheduler = make_scheduler(buddy)
    assert len(scheduler.sort_by_time()) == 1


def test_sort_by_time_no_tasks():
    """A pet with no tasks should return an empty list without crashing."""
    buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    scheduler = make_scheduler(buddy)
    assert scheduler.sort_by_time() == []


# ── filtering ─────────────────────────────────────────────────────────────────

def test_filter_by_pet_name_returns_only_that_pets_tasks():
    buddy    = Pet(name="Buddy",    species="Dog", breed="Labrador", age=3)
    whiskers = Pet(name="Whiskers", species="Cat", breed="Siamese",  age=5)
    buddy.add_task(Task(name="Walk",       category="Exercise", duration_minutes=30, priority=5))
    whiskers.add_task(Task(name="Vet Visit", category="Health",   duration_minutes=45, priority=5))

    scheduler = make_scheduler(buddy, whiskers)
    results = scheduler.filter_tasks(pet_name="Buddy")
    assert all(t.name == "Walk" for t in results)
    assert len(results) == 1


def test_filter_by_completed_false_excludes_done_tasks():
    buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    done    = Task(name="Done Task",    category="Exercise", duration_minutes=10, priority=3, completed=True)
    pending = Task(name="Pending Task", category="Grooming", duration_minutes=10, priority=3)
    buddy.add_task(done)
    buddy.add_task(pending)

    scheduler = make_scheduler(buddy)
    results = scheduler.filter_tasks(completed=False)
    assert all(not t.completed for t in results)
    assert len(results) == 1


def test_filter_no_criteria_returns_all_tasks():
    buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    buddy.add_task(Task(name="A", category="X", duration_minutes=5, priority=1))
    buddy.add_task(Task(name="B", category="X", duration_minutes=5, priority=2))
    scheduler = make_scheduler(buddy)
    assert len(scheduler.filter_tasks()) == 2


# ── recurring tasks ───────────────────────────────────────────────────────────

def test_mark_task_complete_creates_next_daily_occurrence():
    """Completing a daily recurring task should add a new task due tomorrow."""
    buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    today = date.today()
    buddy.add_task(Task(
        name="Morning Walk", category="Exercise", duration_minutes=30,
        priority=5, recurring=True, interval_days=1, due_date=today
    ))
    scheduler = make_scheduler(buddy)
    next_task = scheduler.mark_task_complete("Buddy", "Morning Walk")

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False


def test_mark_task_complete_creates_next_weekly_occurrence():
    """Completing a weekly recurring task should schedule it 7 days later."""
    buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    today = date.today()
    buddy.add_task(Task(
        name="Flea Treatment", category="Grooming", duration_minutes=15,
        priority=4, recurring=True, interval_days=7, due_date=today
    ))
    scheduler = make_scheduler(buddy)
    next_task = scheduler.mark_task_complete("Buddy", "Flea Treatment")

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=7)


def test_mark_task_complete_non_recurring_returns_none():
    """Completing a non-recurring task should NOT create a new task."""
    buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    buddy.add_task(Task(name="One-off Bath", category="Grooming", duration_minutes=20, priority=3))
    scheduler = make_scheduler(buddy)
    result = scheduler.mark_task_complete("Buddy", "One-off Bath")

    assert result is None
    assert len(buddy.get_tasks()) == 1  # no new task added


def test_recurring_task_count_grows_after_completion():
    """Each completion of a recurring task adds one more task to the pet's list."""
    buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    buddy.add_task(Task(
        name="Daily Feed", category="Feeding", duration_minutes=10,
        priority=5, recurring=True, interval_days=1
    ))
    scheduler = make_scheduler(buddy)
    scheduler.mark_task_complete("Buddy", "Daily Feed")
    assert len(buddy.get_tasks()) == 2  # original (done) + new occurrence


# ── conflict detection ────────────────────────────────────────────────────────

def test_detect_conflicts_flags_same_time_cross_pet():
    """Two tasks from different pets at the same time should produce one warning."""
    buddy    = Pet(name="Buddy",    species="Dog", breed="Labrador", age=3)
    whiskers = Pet(name="Whiskers", species="Cat", breed="Siamese",  age=5)
    buddy.add_task(Task(name="Walk",      category="Exercise", duration_minutes=30, priority=5, time="09:00"))
    whiskers.add_task(Task(name="Vet",   category="Health",   duration_minutes=45, priority=5, time="09:00"))

    scheduler = make_scheduler(buddy, whiskers)
    warnings = scheduler.get_conflict_warnings()
    assert len(warnings) == 1
    assert "09:00" in warnings[0]


def test_detect_conflicts_flags_same_time_same_pet():
    """Two tasks for the same pet at the same time should also be flagged."""
    buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    buddy.add_task(Task(name="Walk",  category="Exercise", duration_minutes=30, priority=5, time="14:00"))
    buddy.add_task(Task(name="Train", category="Training", duration_minutes=20, priority=3, time="14:00"))

    scheduler = make_scheduler(buddy)
    warnings = scheduler.get_conflict_warnings()
    assert len(warnings) == 1


def test_detect_conflicts_no_conflicts_returns_empty():
    """Tasks at different times should produce no warnings."""
    buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    buddy.add_task(Task(name="Morning Walk", category="Exercise", duration_minutes=30, priority=5, time="07:00"))
    buddy.add_task(Task(name="Evening Feed", category="Feeding",  duration_minutes=10, priority=4, time="18:00"))

    scheduler = make_scheduler(buddy)
    assert scheduler.get_conflict_warnings() == []


def test_detect_conflicts_unscheduled_tasks_ignored():
    """Tasks with default time '00:00' should not be treated as conflicts."""
    buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    buddy.add_task(Task(name="Task A", category="X", duration_minutes=10, priority=1))
    buddy.add_task(Task(name="Task B", category="X", duration_minutes=10, priority=2))

    scheduler = make_scheduler(buddy)
    assert scheduler.get_conflict_warnings() == []
