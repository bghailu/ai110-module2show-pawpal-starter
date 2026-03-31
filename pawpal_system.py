from dataclasses import dataclass
from datetime import date, datetime, time, timedelta


# ---------------------------------------------------------------------------
# Pet
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    name: str
    species: str


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

@dataclass
class Task:
    name: str
    pet: Pet
    duration_minutes: int
    priority: int          # 1 = high, 2 = medium, 3 = low
    start_time: time | None = None
    reason: str | None = None
    completed: bool = False

    def is_scheduled(self) -> bool:
        return self.start_time is not None

    def schedule(self, start_time: time, reason: str) -> None:
        self.start_time = start_time
        self.reason = reason

    def mark_completed(self) -> None:
        self.completed = True

    def mark_incomplete(self) -> None:
        self.completed = False

    @property
    def end_time(self) -> time | None:
        if self.start_time is None:
            return None
        dt = datetime.combine(date.today(), self.start_time) + timedelta(minutes=self.duration_minutes)
        return dt.time()


# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, name: str, available_start: time, available_end: time):
        self.name = name
        self.available_start = available_start
        self.available_end = available_end

    def available_minutes(self) -> int:
        start = datetime.combine(date.today(), self.available_start)
        end = datetime.combine(date.today(), self.available_end)
        return int((end - start).total_seconds() // 60)


# ---------------------------------------------------------------------------
# DailyPlan
# ---------------------------------------------------------------------------

class DailyPlan:
    def __init__(self, owner: Owner, tasks: list[Task], plan_date: date):
        self.owner = owner
        self.tasks = tasks
        self.plan_date = plan_date

    def generate(self) -> None:
        # Reset any previous scheduling
        for task in self.tasks:
            task.start_time = None
            task.reason = None

        # Sort by priority (1=high first), then by duration (shorter first as tiebreak)
        sorted_tasks = sorted(self.tasks, key=lambda t: (t.priority, t.duration_minutes))

        current_time = datetime.combine(self.plan_date, self.owner.available_start)
        end_time = datetime.combine(self.plan_date, self.owner.available_end)

        for task in sorted_tasks:
            task_end = current_time + timedelta(minutes=task.duration_minutes)
            if task_end <= end_time:
                priority_label = {1: "high", 2: "medium", 3: "low"}.get(task.priority, "unknown")
                reason = (
                    f"Scheduled at {current_time.strftime('%I:%M %p')} — "
                    f"{priority_label} priority task for {task.pet.name} "
                    f"({task.duration_minutes} min)"
                )
                task.schedule(current_time.time(), reason)
                current_time = task_end
            # If it doesn't fit, leave start_time and reason as None

    def scheduled_tasks(self) -> list[Task]:
        return [t for t in self.tasks if t.is_scheduled()]

    def unscheduled_tasks(self) -> list[Task]:
        return [t for t in self.tasks if not t.is_scheduled()]

    def summary(self) -> str:
        lines = [f"Daily Plan for {self.owner.name} — {self.plan_date.strftime('%A, %B %d %Y')}"]
        lines.append(f"Available window: {self.owner.available_start.strftime('%I:%M %p')} – "
                     f"{self.owner.available_end.strftime('%I:%M %p')} "
                     f"({self.owner.available_minutes()} min)\n")

        scheduled = self.scheduled_tasks()
        unscheduled = self.unscheduled_tasks()

        if scheduled:
            lines.append("Scheduled tasks:")
            for task in sorted(scheduled, key=lambda t: t.start_time):
                status = "[x]" if task.completed else "[ ]"
                lines.append(f"  {status} {task.start_time.strftime('%I:%M %p')} – {task.end_time.strftime('%I:%M %p')}"
                             f"  {task.name} ({task.pet.name})")
        else:
            lines.append("No tasks could be scheduled.")

        if unscheduled:
            lines.append("\nCould not fit:")
            for task in unscheduled:
                lines.append(f"  - {task.name} ({task.pet.name}, {task.duration_minutes} min)")

        total = sum(t.duration_minutes for t in scheduled)
        lines.append(f"\nTotal time scheduled: {total} min of {self.owner.available_minutes()} min available.")
        return "\n".join(lines)
