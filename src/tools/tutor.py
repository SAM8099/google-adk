from google.adk.tools import ToolContext


def upload_qa_to_session(tool_context: ToolContext) -> str:
    """Uploads tutor question to  lists in session state."""
    # tool_context.args is a list; args[0] is user answer, args[1] is tutor question
    user_answer = tool_context.args[0] if tool_context.args and len(tool_context.args) > 0 else ""
    tutor_question = tool_context.args[1] if tool_context.args and len(tool_context.args) > 1 else ""

    if "tutor_questions" not in tool_context.state:
        tool_context.state["tutor_questions"] = []

    tool_context.state["tutor_questions"].append(tutor_question)

    return "Tutor question uploaded to session state separately."