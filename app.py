from src.agents.problem_analyzer import create_problem_analyzer_agent
from src.agents.tutor_agent import create_tutor_agent
from src.agents.feedback_agent import create_feedback_agent
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
from src.utils.runners import create_runner
from src.utils.parsers import format_agent_response 
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from src.pipelines.agent_call import call_agent_async
from src.schemas.schemas import SessionInfo, initial_state
from src.utils.utils import add_content, add_user_answer, add_current_problem, add_tutor_question


# Initialize session service
session_service = InMemorySessionService()

APP_NAME = "DSA Tutor"
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create agents and runners
problem_analyzer_root = create_problem_analyzer_agent()
tutor_agent = create_tutor_agent()
feedback_agent = create_feedback_agent()

problem_analyzer_runner = create_runner(agent=problem_analyzer_root, app_name=APP_NAME, session_service=session_service)
tutor_runner = create_runner(agent=tutor_agent, app_name=APP_NAME, session_service=session_service)
feedback_runner = create_runner(agent=feedback_agent, app_name=APP_NAME, session_service=session_service)

active_sessions = {}  # user_id: SessionInfo


@app.post("/create_session")
async def create_session():
    user_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
        state=initial_state.copy(),
    )
    active_sessions[user_id] = SessionInfo(user_id=user_id, session_id=session_id)
    return {
        "status": "success",
        "user_id": user_id,
        "session_id": session_id
    }

@app.post("/set_problem")
async def set_problem(user_id: str, session_id: str, problem: str):
    if user_id not in active_sessions or active_sessions[user_id].session_id != session_id:
        raise HTTPException(status_code=404, detail="Session not found")
    
    await add_current_problem(session_service, APP_NAME, user_id, session_id, problem)
    
    # Call problem analyzer
    analysis_response = await call_agent_async(
        problem_analyzer_runner, user_id, session_id, problem
    )
    analysis_text = format_agent_response(analysis_response)
    
    await add_content(session_service, APP_NAME, user_id, session_id, analysis_text)
    
    return {
        "status": "success",
        "message": "Problem set and analyzed",
        "analysis": analysis_text
    }

@app.post("/process_answer")
async def process_answer(user_id: str, session_id: str, answer: str):
    if user_id not in active_sessions or active_sessions[user_id].session_id != session_id:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get tutor question
    tutor_response = await call_agent_async(tutor_runner, user_id, session_id, answer)
    tutor_question = format_agent_response(tutor_response)
    
    await add_tutor_question(session_service, APP_NAME, user_id, session_id, tutor_question)
    await add_user_answer(session_service, APP_NAME, user_id, session_id, answer)
    
    # Get feedback
    feedback_response = await call_agent_async(feedback_runner, user_id, session_id, answer)
    feedback_text = format_agent_response(feedback_response)
    
    return {
        "status": "success",
        "tutor_question": tutor_question,
        "feedback": feedback_text
    }

@app.get("/session_state")
async def get_session_state(user_id: str, session_id: str):
    if user_id not in active_sessions or active_sessions[user_id].session_id != session_id:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = await session_service.get_session(APP_NAME, user_id, session_id)
    return {
        "status": "success",
        "session_state": session.state
    }

@app.get("/conversation_history")
async def get_conversation_history(user_id: str, session_id: str):
    if user_id not in active_sessions or active_sessions[user_id].session_id != session_id:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = await session_service.get_session(APP_NAME, user_id, session_id)
    tutor_questions = session.state.get("tutor_questions", [])
    user_answers = session.state.get("user_answers", [])
    
    # Zip questions and answers to create conversation pairs
    conversation = []
    for i in range(max(len(tutor_questions), len(user_answers))):
        q = tutor_questions[i] if i < len(tutor_questions) else None
        a = user_answers[i] if i < len(user_answers) else None
        conversation.append({
            "tutor_question": q,
            "user_answer": a
        })
    
    return {
        "status": "success",
        "conversation": conversation
    }