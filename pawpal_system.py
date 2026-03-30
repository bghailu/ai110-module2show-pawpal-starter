from dataclasses import dataclass, field
from datetime import date, time


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

    def is_scheduled(self) -> bool:
        pass

    def schedule(self, start_time: time, reason: str) -> None:
        pass


# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, name: str, available_start: time, available_end: time):
        self.name = name
        self.available_start = available_start
        self.available_end = available_end

    def available_minutes(self) -> int:
        pass


# ---------------------------------------------------------------------------
# DailyPlan
# ---------------------------------------------------------------------------

class DailyPlan:
    def __init__(self, owner: Owner, tasks: list[Task], date: date):
        self.owner = owner
        self.tasks = tasks
        self.date = date

    def generate(self) -> None:
        pass

    def scheduled_tasks(self) -> list[Task]:
        pass

    def unscheduled_tasks(self) -> list[Task]:
        pass

    def summary(self) -> str:
        pass
