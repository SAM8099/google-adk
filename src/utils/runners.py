from google.adk import Runner, InMemorySessionService
from src.agents.problem_analyzer import problem_analyzer_root
from src.agents.tutor_agent import tutor_agent
from src.agents.feedback_agent import feedback_agent

def create_runner(agent, app_name, session_service):
    """Create a Runner instance for the given agent."""
    return Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service,
    )
problem_analyzer_root = create_runner(problem_analyzer_root, "DSA Tutor", InMemorySessionService())
tutor_agent = create_runner(tutor_agent, "DSA Tutor", InMemorySessionService())
feedback_agent = create_runner(feedback_agent, "DSA Tutor", InMemorySessionService())