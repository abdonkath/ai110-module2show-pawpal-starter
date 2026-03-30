# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

Phase 3 added algorithmic intelligence to the `Scheduler` class in `pawpal_system.py`:

| Feature                | Method                              | How it works                                                                                                        |
| ---------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Sort by time**       | `sort_by_time()`                    | Uses `sorted()` with a `lambda` key on `"HH:MM"` strings to return all tasks in chronological order                 |
| **Filter tasks**       | `filter_tasks(pet_name, completed)` | Accepts optional filters for pet name and/or completion status; returns only matching tasks                         |
| **Recurring tasks**    | `mark_task_complete()`              | When a recurring task is completed, automatically creates the next occurrence using `timedelta(days=interval_days)` |
| **Conflict detection** | `get_conflict_warnings()`           | Scans all scheduled tasks for exact time-slot collisions and returns plain-English warning strings                  |

`Task` gained three new optional fields to support these features: `time` (`"HH:MM"`), `recurring` (bool), `interval_days` (int), and `due_date` (`date`).

## Testing PawPal+

### Run the tests

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Group | # Tests | Behaviors verified |
|---|---|---|
| **Task basics** | 2 | Completing a task flips `completed` to `True`; adding a task grows the pet's list |
| **Sorting** | 3 | Tasks return in chronological `HH:MM` order; single task and empty pet don't crash |
| **Filtering** | 3 | Filter by pet name; filter by completion status; no filters returns all tasks |
| **Recurring tasks** | 4 | Daily recurrence schedules next task for tomorrow; weekly for +7 days; non-recurring returns `None`; task count grows after each completion |
| **Conflict detection** | 4 | Cross-pet time clash is flagged; same-pet clash is flagged; different times produce no warning; unscheduled tasks (`"00:00"`) are ignored |

**Total: 16 tests, all passing.**

### Confidence level

⭐⭐⭐⭐ (4/5)

The core scheduling behaviors — sorting, filtering, recurring automation, and conflict detection — are all covered with both happy-path and edge-case tests. One star is held back because conflict detection only checks for exact `HH:MM` matches and does not catch overlapping durations (e.g., a 30-minute task at 09:00 overlapping a task starting at 09:20).

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
