from pawpal_system import Task, Pet, Owner, Scheduler

# Create owner
owner = Owner(name="Alex", available_minutes=90, preferences=["morning walks", "short sessions"])

# Create pets
buddy = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
whiskers = Pet(name="Whiskers", species="Cat", breed="Siamese", age=5)

# Add tasks to Buddy
buddy.add_task(Task(name="Morning Walk",       category="Exercise",   duration_minutes=30, priority=5))
buddy.add_task(Task(name="Flea Treatment",     category="Grooming",   duration_minutes=15, priority=4))
buddy.add_task(Task(name="Training Session",   category="Training",   duration_minutes=20, priority=3))

# Add tasks to Whiskers
whiskers.add_task(Task(name="Vet Check-up",    category="Health",     duration_minutes=45, priority=5))
whiskers.add_task(Task(name="Brush Coat",      category="Grooming",   duration_minutes=10, priority=2))

# Register pets with owner
owner.add_pet(buddy)
owner.add_pet(whiskers)

# Generate and print schedule
scheduler = Scheduler(owner)

print("=" * 50)
print("        TODAY'S PAWPAL SCHEDULE")
print("=" * 50)
print(f"Owner : {owner.name}")
print(f"Time  : {owner.available_minutes} min available")
print(f"Pets  : {', '.join(p.name for p in owner.get_pets())}")
print("-" * 50)

plan = scheduler.generate_plan()
if not plan:
    print("No tasks fit within the available time.")
else:
    total = 0
    for i, task in enumerate(plan, 1):
        priority_label = "[HIGH]  " if task.is_high_priority() else "[normal]"
        status = "done" if task.completed else "pending"
        print(f"  {i}. {priority_label} {task.name:<22} {task.category:<10} {task.duration_minutes:>3} min  ({status})")
        total += task.duration_minutes
    print("-" * 50)
    print(f"  Total scheduled: {total} min  |  Remaining: {owner.available_minutes - total} min")

print("=" * 50)
