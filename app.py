import streamlit as st
import agent_logic
import plan_generator
import progress_tracker

st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #121212;
        color: #e0e0e0;
    }

    .stApp {
        padding: 2rem;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }

    .stContainer {
        background-color: #1e1e1e;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 0 10px rgba(0,0,0,0.4);
    }

    .stExpander {
        background-color: #1b1b1b;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 0.5rem;
    }

    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        margin: 0.2rem;
    }
    .stButton>button:hover {
        background-color: #45a049;
        cursor: pointer;
    }

    textarea, input {
        border-radius: 6px;
        border: 1px solid #555;
        background-color: #1e1e1e;
        color: #e0e0e0;
        padding: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title = "Personalized Learning Coach", layout = "centered")

st.title("Personalized Learning Coach Agent")
st.caption("AI-powered study planner using LLaMA3.2 using Ollama")

st.divider()
tab1, tab2 = st.tabs(["Plan Creator", "Progress Check-in"])

with tab1:
    st.subheader("Plan Creator")

    st.markdown("#### Define Your Learning Goal")
    topic = st.text_input("What do you want to learn?", placeholder = "e.g. Learn Backend Web Development")

    if st.button("Break Down Topic"):
        if topic.strip():
            with st.spinner("Generating subtopics..."):
                subtopics = agent_logic.break_down_topic(topic)
                st.success("Subtopics generated successfully!")
                with st.expander("View Subtopics", expanded = True):
                    st.text(subtopics)
                st.session_state["subtopics"] = subtopics
        else:
            st.warning("Please enter a learning goal to proceed.")

    if "subtopics" in st.session_state:
        st.divider()
        st.markdown("#### Study Plan Configuration")
        duration_weeks = st.number_input("Duration (weeks)", min_value = 1, max_value = 12, value = 4)
        
        if st.button("Generate Study Plan"):
            with st.spinner("Creating your personalized study plan..."):
                plan = agent_logic.generate_study_plan(st.session_state["subtopics"], duration_weeks)
                st.success("Study Plan generated successfully!")
                with st.expander("View Study Plan", expanded = True):
                    st.text(plan)
                st.session_state["plan"] = plan

    if "plan" in st.session_state:
        st.divider()
        st.markdown("#### Manage Saved Plan")
        cols = st.columns(3)
        with cols[0]:
            if st.button("Save Plan"):
                plan_generator.save_plan(st.session_state.get("subtopics", ""), st.session_state.get("plan", ""))
                st.success("Plan saved successfully!")
        with cols[1]:
            if st.button("Load Saved Plan"):
                subtopics, plan = plan_generator.load_plan()
                if subtopics or plan:
                    st.session_state["subtopics"] = subtopics
                    st.session_state["plan"] = plan
                    st.success("Loaded saved plan!")
                else:
                    st.warning("No saved plan found.")
        with cols[2]:
            if st.button("Reset Saved Plan"):
                plan_generator.reset_plan()
                st.session_state.pop("subtopics", None)
                st.session_state.pop("plan", None)
                st.success("Saved plan has been reset.")

with tab2:
    st.subheader("Progress Check-in")

    st.markdown("#### Current Study Plan")
    current_plan = st.text_area("Paste your current study plan:", value = st.session_state.get("plan", ""), height = 200)

    st.markdown("#### Progress Notes")
    progress_notes = st.text_area("Your progress notes / issues:", height = 150)

    if st.button("Adjust Plan"):
        if current_plan.strip() and progress_notes.strip():
            with st.spinner("Adjusting plan based on your progress..."):
                new_plan = agent_logic.adjust_plan(current_plan, progress_notes)
                st.success("Updated Plan generated!")
                with st.expander("View Updated Plan", expanded = True):
                    st.text(new_plan)
        else:
            st.warning("Please fill in both the current plan and your progress notes.")

    st.divider()
    st.markdown("#### Manage Progress Notes")
    cols2 = st.columns(3)
    with cols2[0]:
        if st.button("Save Progress Note"):
            if progress_notes.strip():
                progress_tracker.save_progress_note(progress_notes)
                st.success("Progress note saved!")
            else:
                st.warning("Please enter your progress notes to save.")
    with cols2[1]:
        if st.button("Load All Progress Notes"):
            notes = progress_tracker.load_progress_notes()
            if notes:
                st.success(f"Loaded {len(notes)} notes!")
                for entry in notes:
                    with st.expander(f"{entry['timestamp']}"):
                        st.text(entry['note'])
            else:
                st.warning("No progress notes found.")
    with cols2[2]:
        if st.button("Reset Progress Notes"):
            progress_tracker.reset_progress_notes()
            st.success("All progress notes have been deleted.")
