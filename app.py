import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Initialize Owner in session state once — persists across reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=90)

st.title("PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# ── Add a Pet ─────────────────────────────────────────────────────────────────
st.subheader("Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["Dog", "Cat", "Other"])
with col3:
    age = st.number_input("Age", min_value=0, max_value=30, value=2)

if st.button("Add Pet"):
    existing = [p.name for p in st.session_state.owner.get_pets()]
    if pet_name in existing:
        st.warning(f"{pet_name} is already added.")
    else:
        st.session_state.owner.add_pet(Pet(name=pet_name, species=species, breed="", age=int(age)))
        st.success(f"Added {pet_name} the {species}!")

pets = st.session_state.owner.get_pets()
if pets:
    st.write("**Pets:**", ", ".join(p.name for p in pets))

st.divider()

# ── Add a Task ────────────────────────────────────────────────────────────────
st.subheader("Add a Task")
if not pets:
    st.info("Add a pet first before scheduling tasks.")
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        target_pet = st.selectbox("For pet", [p.name for p in pets])
    with col2:
        task_title = st.text_input("Task name", value="Morning walk")
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.slider("Priority (1-5)", min_value=1, max_value=5, value=3)

    if st.button("Add Task"):
        pet_obj = next(p for p in pets if p.name == target_pet)
        pet_obj.add_task(Task(name=task_title, category="General", duration_minutes=int(duration), priority=priority))
        st.success(f"Added '{task_title}' to {target_pet}.")

    for pet in pets:
        if pet.get_tasks():
            st.markdown(f"**{pet.name}'s tasks:**")
            st.table([{"Task": t.name, "Duration (min)": t.duration_minutes, "Priority": t.priority, "Done": t.completed} for t in pet.get_tasks()])

st.divider()

# ── Generate Schedule ─────────────────────────────────────────────────────────
st.subheader("Build Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler(st.session_state.owner)
    plan = scheduler.generate_plan()
    if not plan:
        st.warning("No tasks fit within the available time, or no tasks added yet.")
    else:
        total = sum(t.duration_minutes for t in plan)
        st.success(f"Scheduled {len(plan)} task(s) — {total} min used.")
        st.table([{"Task": t.name, "Duration (min)": t.duration_minutes, "Priority": t.priority, "High Priority": t.is_high_priority()} for t in plan])
