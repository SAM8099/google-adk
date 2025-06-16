import asyncio
from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from src.agents.problem_analyzer import problem_analyzer_root
from src.agents.tutor_agent import tutor_agent
from src.agents.feedback_agent import feedback_agent
from src.utils.utils import add_content, add_user_answer, add_current_problem, add_tutor_question
from src.pipelines.agent_call import call_agent_async

from src.schemas.schemas import initial_state

session_service = InMemorySessionService()

async def main_async():
    APP_NAME = "DSA Tutor"
    USER_ID = "RANDOM_USER_ID"  # Replace with actual user ID or logic to generate one

    # Create a new session with initial state
    new_session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    SESSION_ID = new_session.id
    print(f"Created new session: {SESSION_ID}")

    # Create separate runners for each agent
    problem_analyzer_runner = Runner(
        agent=problem_analyzer_root,
        app_name=APP_NAME,
        session_service=session_service,
    )
    tutor_runner = Runner(
        agent=tutor_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    feedback_runner = Runner(
        agent=feedback_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    feedback_response = None
    print("\nWelcome to the DSA Tutor System!")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while feedback_response is None or feedback_response.content.parts[0].text.strip().lower() != "exit":
        session = session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
        current_problem = session.state.get("current_problem", None)

        if current_problem is None:
            print("Please set a DSA problem to begin.")
            user_input = input("Enter problem (or 'exit' to quit): ")
            
            if user_input.lower() in ["exit", "quit"]:
                print("Ending session. Goodbye!")
                break
                
            # Update problem and history
            add_current_problem(
                session_service, APP_NAME, USER_ID, SESSION_ID, user_input
            )
            # Update current problem in session state
            updated_state = session.state.copy()
            updated_state["current_problem"] = user_input
            session_service.create_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=SESSION_ID,
                state=updated_state,
            )
            problem_analyzer_response = await call_agent_async(
                problem_analyzer_runner, USER_ID, SESSION_ID, user_input
            )
            add_content(
                session_service, APP_NAME, USER_ID, SESSION_ID, problem_analyzer_response
            )
        # Get user input
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break


        # Process with tutor agent
        tutor_question = await call_agent_async(tutor_runner, USER_ID, SESSION_ID, user_input)
        
        await add_tutor_question(
            session_service, APP_NAME, USER_ID, SESSION_ID, tutor_question
        )
        # Get feedback agent decision
        user_answer = input(f"Tutor: {tutor_question}\nYour answer: ")
        if user_answer.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break
        else:
            print("Processing your answer...")
        feedback_response = await call_agent_async(feedback_runner, USER_ID, SESSION_ID, user_input)
        add_user_answer(
            session_service, APP_NAME, USER_ID, SESSION_ID, user_answer
        )
        
        # Check feedback decision
        if feedback_response and feedback_response.content.parts[0].text.strip().lower() == "exit":
            print("\nSystem: Session completed successfully!")
            break

    # Show final session state
    final_session = session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print("\nFinal Session State:")
    for key, value in final_session.state.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    asyncio.run(main_async())
