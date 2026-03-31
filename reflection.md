# PawPal+ Project Reflection

## 1. System Design
1. Edit schedule
2. See medication
3. Schedule a grooming

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Owner holds the user's time constraints and knows how much time is available in a day. An Owner can have multiple Pet objects, each representing a single animal with basic identity info. A Task belongs to one Pet and captures what needs to be done, how long it takes, and how urgent it is — it also holds its own scheduled time once assigned. DailyPlan is the central coordinator: given an Owner and a list of Task objects, it runs the scheduling logic, assigns start times to tasks that fit within the owner's window, and can produce a human-readable summary of the result.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes it changed multiple times when I was adding new fretures. For example Task needed to have a recurring and non recurring version. So I have added new attributes and methods for that change.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

I used AI mainly for two things: talking through the initial class design before writing any code, and speeding up repetitive implementation work like adding filtering and sorting methods. The most useful prompts were specific ones — asking "given this class structure, what's the cleanest way to handle recurring tasks?" got better results than broad questions like "help me with scheduling."

**b. Judgment and verification**

When the AI first suggested how to handle recurring tasks, it proposed a separate `RecurringTask` subclass. I didn't accept that because it would have complicated the filtering and scheduling logic that already worked on a flat list of `Task` objects. Instead I kept a single class and added `frequency` as an optional attribute, which was simpler and still covered the use case.

---

## 4. Testing and Verification

**a. What you tested**

I tested that the scheduler respects priority order, that tasks exceeding the available window are left unscheduled rather than overflow, that completing a recurring task produces a new instance with the correct next due date, and that conflict detection flags overlapping tasks.

These tests mattered because the scheduling and recurrence logic are the core of the app — if those are wrong, the daily plan output is meaningless regardless of how good the UI looks.

**b. Confidence**

I'm confident in the happy-path cases that are covered by tests. I'm less confident around edge cases like tasks that exactly fill the remaining window (boundary arithmetic), or what happens if an owner's start and end times span midnight. I'd test those next.

---

## 5. Reflection

**a. What went well**

The class structure held up well as features were added. Keeping `Task` responsible for its own scheduling state (start time, completion, next occurrence) meant `DailyPlan` stayed focused on coordination rather than managing task details directly.

**b. What you would improve**

I'd add the ability to edit or reorder tasks after they've been added instead of only being able to remove them. Right now fixing a mistake means deleting a task and re-entering it, which is clunky.

**c. Key takeaway**

AI is most useful as a collaborator on design decisions when you already have a partial mental model to push back with. If you accept suggestions passively without running them against the actual constraints of your system, you end up with code that's locally reasonable but doesn't fit together well.
