from google.adk.tools import ToolContext

def upload_analyst_context(tool_context: ToolContext) -> str:
    """Uploads the analysis context to the session state."""
    # tool_context.args is a list; take the first argument as context
    context = tool_context.args[0] if tool_context.args and len(tool_context.args) > 0 else ""
    tool_context.state["analyst_context"] = context
    return "Analysis context uploaded to session state."