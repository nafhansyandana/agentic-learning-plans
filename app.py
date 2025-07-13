import streamlit as st
import agent_logic

st.set_page_config(page_title="Personalized Learning Coach", layout = "centered")

st.title("Personalized Learning Coach Agent")
st.subheader("AI-powered study planner using LLaMA3 using Ollama")

tab1, tab2 = st.tabs(["Plan Creator", "Progress Check-in"])

with tab1:
    st.header("[1] Plan Creator")

    # Input learning goal
    topic = st.text_input("What do you want to learn?", placeholder = "e.g. Learn Backend Web Development")

    if st.button("Break Down Topic"):
        if topic.strip():
            with st.spinner("Generating subtopics..."):
                subtopics = agent_logic.break_down_topic(topic)
                st.success("Subtopics generated!")
                st.text_area("Subtopics:", subtopics, height=200)
                st.session_state["subtopics"] = subtopics
        else:
            st.warning("Please enter a learning goal.")

    # Generate study plan
    if "subtopics" in st.session_state:
        duration_weeks = st.number_input("Duration (weeks)", min_value = 1, max_value = 12, value = 4)
        if st.button("Generate Study Plan"):
            with st.spinner("Creating study plan..."):
                plan = agent_logic.generate_study_plan(st.session_state["subtopics"], duration_weeks)
                st.success("Study Plan generated!")
                st.text_area("Study Plan:", plan, height = 300)
                st.session_state["plan"] = plan


with tab2:
    st.header("[2] Progress Check-in")

    current_plan = st.text_area("Paste your current study plan:", value = st.session_state.get("plan", ""))
    progress_notes = st.text_area("Your progress notes / issues:", height = 150)

    if st.button("Adjust Plan"):
        if current_plan.strip() and progress_notes.strip():
            with st.spinner("Adjusting plan based on progress..."):
                new_plan = agent_logic.adjust_plan(current_plan, progress_notes)
                st.success("Updated Plan!")
                st.text_area("Updated Plan:", new_plan, height = 300)
        else:
            st.warning("Please fill in both the current plan and your progress notes.")
