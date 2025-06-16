from datetime import datetime

def add_current_problem(session_service, app_name, user_id, session_id, text):
    """Add or update the current problem in the session state."""
    try:
        session = session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
        updated_state = session.state.copy()
        updated_state["current_problem"] = text
    except Exception as e:
        print(f"Error updating current_problem: {e}")

def add_tutor_question(session_service, app_name, user_id, session_id, text):
    """Append a tutor question to the tutor_questions list in the session state."""
    try:
        session = session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
        updated_state = session.state.copy()
        if "tutor_questions" not in updated_state:
            updated_state["tutor_questions"] = []
        updated_state["tutor_questions"].append(text)

    except Exception as e:
        print(f"Error updating tutor_questions: {e}")

def add_user_answer(session_service, app_name, user_id, session_id, text):
    """Append a user answer to the user_answers list in the session state."""
    try:
        session = session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
        updated_state = session.state.copy()
        if "user_answers" not in updated_state:
            updated_state["user_answers"] = []
        updated_state["user_answers"].append(text)
        session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state=updated_state,
        )
    except Exception as e:
        print(f"Error updating user_answers: {e}")

def add_content(session_service, app_name, user_id, session_id, text):
    """Add or update the content field in the session state."""
    try:
        session = session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
        updated_state = session.state.copy()
        updated_state["content"] = text
    except Exception as e:
        print(f"Error updating content: {e}")


