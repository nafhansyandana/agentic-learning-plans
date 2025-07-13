from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from config import OLLAMA_MODEL

llm = Ollama(model=OLLAMA_MODEL)

# Break down topic
def break_down_topic(topic: str) -> str:
    prompt = f"""
    You are a helpful learning coach. Please break down the following topic into detailed subtopics for a student to study.
    Topic: {topic}
    Respond as a bullet list of subtopics.
    """
    return llm.invoke(prompt)

# Generate study plan
def generate_study_plan(subtopics: str, duration_weeks: int) -> str:
    prompt = f"""
    You are an AI learning planner. Please create a detailed {duration_weeks}-week study plan for these subtopics: {subtopics}
    For each week, specify which subtopics to cover and daily goals if possible.
    """
    return llm.invoke(prompt)

# Adjust plan
def adjust_plan(current_plan: str, progress_notes: str) -> str:
    prompt = f"""
    You are an adaptive learning coach. Here is the student's current study plan: {current_plan}
    And here are their progress notes: {progress_notes}
    Please suggest an updated plan based on this progress. Be encouraging and helpful.
    """
    return llm.invoke(prompt)
