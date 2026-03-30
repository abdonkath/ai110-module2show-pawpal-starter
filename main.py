from pawpal_system import Task, Pet, Owner, Scheduler

# Create owner
owner = Owner(name="Alex", available_minutes=90, preferences=["morning walks", "short sessions"])

# Create pets
buddy    = Pet(name="Buddy",    species="Dog", breed="Labrador", age=3)
whiskers = Pet(name="Whiskers", species="Cat", breed="Siamese",  age=5)

# Add tasks OUT OF ORDER (time-wise) to demonstrate sorting
buddy.add_task(Task(name="Evening Brushing",  category="Grooming",  duration_minutes=10,
                    priority=2, time="18:30", recurring=True,  interval_days=2))
buddy.add_task(Task(name="Morning Walk",      category="Exercise",  duration_minutes=30,
                    priority=5, time="07:00", recurring=True,  interval_days=1))
buddy.add_task(Task(name="Flea Treatment",    category="Grooming",  duration_minutes=15,
                    priority=4, time="09:00"))
buddy.add_task(Task(name="Training Session",  category="Training",  duration_minutes=20,
                    priority=3, time="14:00"))

whiskers.add_task(Task(name="Vet Check-up",   category="Health",    duration_minutes=45,
                        priority=5, time="09:00"))   # same time as Flea Treatment → conflict!
whiskers.add_task(Task(name="Brush Coat",     category="Grooming",  duration_minutes=10,
                        priority=2, time="11:00", recurring=True, interval_days=3))

# Register pets with owner
owner.add_pet(buddy)
owner.add_pet(whiskers)

scheduler = Scheduler(owner)

# ── Original priority-based plan ──────────────────────────────────────────────
print("=" * 55)
print("        TODAY'S PAWPAL SCHEDULE  (by priority)")
print("=" * 55)
plan = scheduler.generate_plan()
total = 0
for i, task in enumerate(plan, 1):
    label  = "[HIGH]  " if task.is_high_priority() else "[normal]"
    status = "done" if task.completed else "pending"
    print(f"  {i}. {label} {task.name:<22} {task.category:<10}"
          f" {task.duration_minutes:>3} min  ({status})")
    total += task.duration_minutes
print("-" * 55)
print(f"  Total scheduled: {total} min  |  Remaining: {owner.available_minutes - total} min")

# ── Sorted by time ────────────────────────────────────────────────────────────
print()
print("=" * 55)
print("        TASKS SORTED BY TIME")
print("=" * 55)
for task in scheduler.sort_by_time():
    status = "done" if task.completed else "pending"
    print(f"  {task.time}  {task.name:<22} [{status}]")

# ── Filter: Buddy's tasks only ────────────────────────────────────────────────
print()
print("=" * 55)
print("        FILTER: BUDDY'S TASKS")
print("=" * 55)
for task in scheduler.filter_tasks(pet_name="Buddy"):
    print(f"  {task.time}  {task.name:<22} priority={task.priority}")

# ── Filter: incomplete tasks ──────────────────────────────────────────────────
print()
print("=" * 55)
print("        FILTER: INCOMPLETE TASKS (all pets)")
print("=" * 55)
for task in scheduler.filter_tasks(completed=False):
    print(f"  {task.name:<22} category={task.category}")

# ── Recurring tasks ───────────────────────────────────────────────────────────
print()
print("=" * 55)
print("        RECURRING TASKS")
print("=" * 55)
recurring = scheduler.get_recurring_tasks()
if recurring:
    for task in recurring:
        print(f"  {task.name:<22} every {task.interval_days} day(s)")
else:
    print("  No recurring tasks found.")

# ── Conflict detection ────────────────────────────────────────────────────────
print()
print("=" * 55)
print("        SCHEDULE CONFLICTS")
print("=" * 55)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for a, b in conflicts:
        print(f"  !! {a.name} vs {b.name}  (both at {a.time})")
else:
    print("  No conflicts found.")

print("=" * 55)
