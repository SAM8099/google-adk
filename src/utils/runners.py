from google.adk import Runner

def create_runner(agent, app_name, session_service):
    """Create a Runner instance for the given agent."""
    return Runner(
        agent=agent,
        app_name=app_name,
        session_service=session_service,
    )
