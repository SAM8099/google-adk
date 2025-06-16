from google.adk import Agent, AgentConfig, Response, AgentState, Runner
from google.adk.tools import google_search_tool
from src.tools.problem_analyst import upload_analyst_context

from src.agents.feedback_agent import feedback_agent
from src.agents.content_agent import content_agent
from src.agents.tutor_agent import tutor_agent
from src.utils.utils import add_problem_to_history
problem_analyzer_root = Agent(
    name="Problem Analyzer",
    model="gemini-2.0-flash",
    description="Analyzes problems and creates context to direct it to tutor agent.",  
    instructions="""Analyze the user's question and extract relevant DSA concepts. 
            Use the 'google_search_tool' to find relevant content and the 'upload_analyst_context' tool to save your analysis to the session state.
        """,
        tools=[google_search_tool, upload_analyst_context]  # Assuming google_search_tool is defined elsewhere
)
