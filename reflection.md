# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
  The UML diagram models a pet care scheduling system w/ 4 classes connected. If Owner has 1 or more Pets, each Pet has a list of Tasks, and a Scheduler bring them to together to create a daily care plan. It is based on the owner's available time and each task's prioruty and duration.
  I included:
  Owner: stores pet owner's name, time availability, and care preferences
  Pets: stores pet's basic info like name, species, and age
  Task: represents the activity like walking, feeding, meds and more. It also has duration and priority level. It tracks if the task has been completed or not
  Scheduler: Takes Owner and Pet as input and creates a prioritized daily plan that fits w/ owner available time

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Originally, the Scheduler was planned to consider the owner's preferences (like "morning walks") when building the plan. During implementation, I simplified this by the generate_plan() method only filters by priority and available time, ignoring preferences. I made this tradeoff because matching free-text preferences to task names added complexity that wasn't needed to get a working schedule. I also added a category field to Task that wasn't in the original UML, since it made the schedule output more readable and helped group tasks logically.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

The conflict detection only flags tasks that share an **exact** `HH:MM` start time — it does not check whether two tasks _overlap_ in duration. For example, a 30-minute walk at 09:00 and a 15-minute vet visit at 09:20 would not be flagged, even though they overlap in real life.

This is a reasonable tradeoff for a first version because:

- Exact-match comparisons are simple string equality (`task_a.time == task_b.time`), requiring no time parsing or arithmetic.
- Most pet-care schedules are planned in clear, non-overlapping blocks, so exact-time collisions catch the most common mistake.
- Adding overlap detection would require converting `"HH:MM"` strings to `datetime` objects, computing end times from `duration_minutes`, and checking range intersections — significantly more complexity for an edge case most users won't hit.

A future improvement would use `datetime.strptime` to parse times and compare `[start, start + duration)` intervals instead.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
  I use AI for brainstorming, implementating, and generating test file. I ensure to be specific on the edge case, for example, empty pets, non-recurring tasks, and unscheduled "00:00" times. The prompts that are good are specific ones. If response is unclear, I asked for follow-up questions and even asking it to explain like I'm 10 so I can understand the concept more clearly.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
  AI originally added mark_task_complete() in Task class but Task shouldn't know about pets or to add itself to back to list. I decided to put it in Scheduler instead where it should look up right pet, mark task done, and call pet.add_task().

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
  I tested sorting, recurring task automation, and conflict detection.

Sorting: I had to make sure that the task added are in chronological order
Recurring Task: I ensure that completing a daily task created a new one due the next day, and a weekly task pushed it forward 7 days
Conflict detection: I tested both same-pet and cross-pet time collisions, and also verified that unscheduled tasks with the default "00:00" time were never flagged as conflicts

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm 90% confident that my scheduler works.My main uncertainty is around the conflict detection not catching overlapping durations, which I mentioned as a tradeoff.

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
  The most satisfying part is putting the pieces together and building the UI in streamlit.
  **b. What you would improve**

- If you had another iteration, what would you improve or redesign?
  I would upgrade conflict detection to check overlapping durations instead of just exact start times a 30-minute walk at 09:00 and a vet visit at 09:20 should both trigger a warning.
  **c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
  The most important thing I learned is that AI is most useful when you already have a clear design. When I gave vague prompts, the suggestions were generic and sometimes put logic in the wrong class like when it tried to put mark_task_complete inside Task instead of Scheduler. But when I understood the class responsibilities from the UML diagram first, I could give precise prompts and immediately spot when a suggestion violated the design. AI accelerated the writing, but the thinking still had to come first.
