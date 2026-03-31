import streamlit as st
from datetime import date, time
import pawpal_system as ps

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ---------------------------------------------------------------------------
# Owner & Pet
# ---------------------------------------------------------------------------
st.subheader("Owner & Pet")

col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
    avail_start = st.time_input("Available from", value=time(8, 0))
    avail_end = st.time_input("Available until", value=time(18, 0))
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Set Owner & Pet"):
    st.session_state.owner = ps.Owner(
        name=owner_name,
        available_start=avail_start,
        available_end=avail_end,
    )
    st.session_state.pet = ps.Pet(name=pet_name, species=species)
    st.session_state.tasks = []          # reset tasks when owner/pet changes
    st.success(f"Saved: {owner_name} with pet {pet_name} ({species})")

if "owner" in st.session_state:
    o = st.session_state.owner
    p = st.session_state.pet
    st.caption(
        f"Active: **{o.name}** | {p.name} ({p.species}) | "
        f"{o.available_start.strftime('%I:%M %p')} – {o.available_end.strftime('%I:%M %p')} "
        f"({o.available_minutes()} min available)"
    )

st.divider()

# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------
st.subheader("Tasks")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "owner" not in st.session_state:
    st.info("Set an owner and pet above before adding tasks.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority_label = st.selectbox("Priority", ["high", "medium", "low"])

    if st.button("Add task"):
        priority_map = {"high": 1, "medium": 2, "low": 3}
        task = ps.Task(
            name=task_title,
            pet=st.session_state.pet,
            duration_minutes=int(duration),
            priority=priority_map[priority_label],
        )
        st.session_state.tasks.append(task)

    if st.session_state.tasks:
        st.write("Current tasks:")
        priority_names = {1: "high", 2: "medium", 3: "low"}
        rows = [
            {
                "Task": t.name,
                "Pet": t.pet.name,
                "Duration (min)": t.duration_minutes,
                "Priority": priority_names[t.priority],
            }
            for t in st.session_state.tasks
        ]
        st.table(rows)
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# ---------------------------------------------------------------------------
# Generate Schedule
# ---------------------------------------------------------------------------
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if "owner" not in st.session_state:
        st.warning("Set an owner and pet first.")
    elif not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        plan = ps.DailyPlan(
            owner=st.session_state.owner,
            tasks=list(st.session_state.tasks),
            plan_date=date.today(),
        )
        plan.generate()
        st.text(plan.summary())

        unscheduled = plan.unscheduled_tasks()
        if unscheduled:
            st.warning(f"{len(unscheduled)} task(s) didn't fit in the available window.")
