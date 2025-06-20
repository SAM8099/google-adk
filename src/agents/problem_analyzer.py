from google.adk import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

search_tool= GoogleSearchTool()
def create_problem_analyzer_agent():
    """Create and return the Problem Analyzer agent."""
    return Agent(
        name="Problem_Analyzer",
        model="gemini-2.0-flash",
        description="Analyzes problems and creates context to direct it to tutor agent.",
        instruction="""Analyze the user's question and extract relevant DSA concepts. 
            Use the 'google_search_tool' to find relevant content.
        """,
        tools=[search_tool]  # Assuming google_search_tool is defined elsewhere
    )


