from google.adk import Agent
from src.tools.tutor import upload_qa_to_session

def create_tutor_agent():
    """Create and return the Tutor Agent."""
    return Agent(
        name="Tutor_Agent",     
        model="gemini-2.0-flash",
        description="An expert Socratic tutor for Data Structures and Algorithms, guiding students through problem-solving without giving direct answers.",
        instruction="""
        You are a Socratic tutor for Data Structures and Algorithms.
        Current problem: {current_problem}
        Previous questions: {tutor_questions}
        Previous answers: {user_answers}
        Content summary: {content}

        Guidelines:
        1. NEVER repeat previous questions
        2. Build on the student's last response
        3. Ask progressively deeper questions
        4. Never give direct answers or code solutions
    """,
        tools=[upload_qa_to_session],  # Assuming upload_qa_to_session is defined in src/tools/__init__.py
    )
    

