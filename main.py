from datetime import date, time
from pawpal_system import Owner, Pet, Task, DailyPlan


owner = Owner(
    name="Alex",
    available_start=time(8, 0),   # 8:00 AM
    available_end=time(18, 0),    # 6:00 PM
)

dog = Pet(name="Buddy", species="dog")
cat = Pet(name="Miso", species="cat")

tasks = [
    Task(name="Morning walk",     pet=dog, duration_minutes=30, priority=1),
    Task(name="Feed breakfast",   pet=dog, duration_minutes=10, priority=1),
    Task(name="Clean litter box", pet=cat, duration_minutes=10, priority=2),
    Task(name="Flea medication",  pet=cat, duration_minutes=5,  priority=1),
    Task(name="Enrichment play",  pet=dog, duration_minutes=20, priority=3),
    Task(name="Brushing",         pet=dog, duration_minutes=15, priority=3),
]

plan = DailyPlan(owner=owner, tasks=tasks, plan_date=date.today())
plan.generate()

# Manually force a conflict: override Enrichment play to overlap with Brushing
enrichment = next(t for t in tasks if t.name == "Enrichment play")
enrichment.schedule(time(8, 5), "manually scheduled — overlaps with Feed breakfast")

print(plan.summary())

print("\n--- Conflict Check ---")
conflicts = plan.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"WARNING: {warning}")
else:
    print("No conflicts detected.")
