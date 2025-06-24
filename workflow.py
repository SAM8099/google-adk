import asyncio
from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from src.agents.problem_analyzer import create_problem_analyzer_agent
from src.agents.tutor_agent import create_tutor_agent
from src.agents.feedback_agent import create_feedback_agent
from src.utils.utils import add_content, add_user_answer, add_current_problem, add_tutor_question
from src.pipelines.agent_call import call_agent_async
from src.schemas.schemas import initial_state

problem_analyzer_root = create_problem_analyzer_agent()
tutor_agent = create_tutor_agent()
feedback_agent = create_feedback_agent()

session_service = InMemorySessionService()

async def main_async():
    APP_NAME = "DSA Tutor"
    USER_ID = "RANDOM_USER_ID"

    # Create session
    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state.copy(),
    )
    SESSION_ID = new_session.id
    print(f"Created new session: {SESSION_ID}")

    # Create agent runners
    problem_analyzer_runner = Runner(agent=problem_analyzer_root, app_name=APP_NAME, session_service=session_service)
    tutor_runner = Runner(agent=tutor_agent, app_name=APP_NAME, session_service=session_service)
    feedback_runner = Runner(agent=feedback_agent, app_name=APP_NAME, session_service=session_service)
    
    print("\nWelcome to the DSA Tutor System!")
    print("Type 'exit' or 'quit' to end the conversation.\n")
    print("You can set a DSA problem to begin. The system will guide you through the process.")
    
    # Get initial problem
    problem = input("Enter problem (or 'exit' to quit): ")
    if problem.lower() in ["exit", "quit"]:
        print("Ending session. Goodbye!")
        return

    # Process initial problem
    await add_current_problem(session_service, APP_NAME, USER_ID, SESSION_ID, problem)
    analysis = await call_agent_async(problem_analyzer_runner, USER_ID, SESSION_ID, problem)
    await add_content(session_service, APP_NAME, USER_ID, SESSION_ID, analysis)

    # Generate first tutor question
    tutor_question = await call_agent_async(tutor_runner, USER_ID, SESSION_ID, "Start the tutoring session")
    print(f"\nTutor: {tutor_question}")
    await add_tutor_question(session_service, APP_NAME, USER_ID, SESSION_ID, tutor_question)

    # Main tutoring loop
    while True:
        # Get user answer to tutor's question
        user_answer = input("Your answer: ")
        if user_answer.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break
            
        await add_user_answer(session_service, APP_NAME, USER_ID, SESSION_ID, user_answer)
        
        # Get feedback
        feedback_context = f"TUTOR QUESTION: {tutor_question}\nUSER ANSWER: {user_answer}"
        feedback_response = await call_agent_async(feedback_runner, USER_ID, SESSION_ID, feedback_context)
        
        # Process feedback
        if feedback_response and hasattr(feedback_response, "content") and hasattr(feedback_response.content, "parts"):
            feedback_text = feedback_response.content.parts[0].text.strip().lower()
            if "exit" in feedback_text:
                print("\nSystem: Session completed successfully!")
                break

        # Generate next tutor question based on user's answer
        tutor_question = await call_agent_async(tutor_runner, USER_ID, SESSION_ID, user_answer)
        print(f"\nTutor: {tutor_question}")
        await add_tutor_question(session_service, APP_NAME, USER_ID, SESSION_ID, tutor_question)

    # Show final state
    final_session = await session_service.get_session(SESSION_ID)
    print("\nFinal Session State:")
    for key, value in final_session.state.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    asyncio.run(main_async())
