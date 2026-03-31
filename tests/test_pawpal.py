from datetime import date, time
from pawpal_system import Owner, Pet, Task, DailyPlan


# ---------------------------------------------------------------------------
# Test 1: mark_completed() changes the task's completed status
# ---------------------------------------------------------------------------

def test_mark_completed_changes_status():
    pet = Pet(name="Buddy", species="dog")
    task = Task(name="Morning walk", pet=pet, duration_minutes=30, priority=1)

    assert task.completed is False
    task.mark_completed()
    assert task.completed is True


# ---------------------------------------------------------------------------
# Test 2: adding a task for a pet increases that pet's task count in the plan
# ---------------------------------------------------------------------------

def test_adding_task_increases_pet_task_count():
    owner = Owner(name="Alex", available_start=time(8, 0), available_end=time(18, 0))
    dog = Pet(name="Buddy", species="dog")

    plan = DailyPlan(owner=owner, tasks=[], plan_date=date.today())

    def tasks_for(pet):
        return [t for t in plan.tasks if t.pet == pet]

    assert len(tasks_for(dog)) == 0

    plan.tasks.append(Task(name="Morning walk", pet=dog, duration_minutes=30, priority=1))
    assert len(tasks_for(dog)) == 1

    plan.tasks.append(Task(name="Feed breakfast", pet=dog, duration_minutes=10, priority=1))
    assert len(tasks_for(dog)) == 2
