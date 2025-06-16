from src.agents.problem_analyzer import problem_analyzer_root
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.pipelines.workflow import main_async
import asyncio
from fastapi import HTTPException
from src.utils.utils import add_content, add_user_answer, add_current_problem, add_tutor_question
import uuid
from src.pipelines.workflow import session_service , main_async
from src.agents.tutor_agent import tutor_agent
from src.agents.feedback_agent import feedback_agent
from src.pipelines.agent_call import call_agent_async
from src.pipelines.workflow import initial_state


APP_NAME = "DSA Tutor"
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class SessionInfo:
    def __init__(self, user_id, session_id):
        self.user_id = user_id
        self.session_id = session_id

active_sessions = {}  # user_id: SessionInfo

@app.post("/create_session")
async def create_session():
    user_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
        state=initial_state.copy(),
    )
    active_sessions[user_id] = SessionInfo(user_id, session_id)
    return {"user_id": user_id, "session_id": session_id}

@app.post("/set_problem")
async def set_problem(user_id: str, session_id: str, problem: str):
    if user_id not in active_sessions or active_sessions[user_id].session_id != session_id:
        raise HTTPException(status_code=404, detail="Session not found")
    add_current_problem(session_service, APP_NAME, user_id, session_id, problem)
    # Call problem analyzer and store content
    analysis = await call_agent_async(problem_analyzer_runner, user_id, session_id, problem)
    add_content(session_service, APP_NAME, user_id, session_id, analysis)
    return {"status": "Problem set and analyzed"}

@app.post("/process_answer")
async def process_answer(user_id: str, session_id: str, answer: str):
    if user_id not in active_sessions or active_sessions[user_id].session_id != session_id:
        raise HTTPException(status_code=404, detail="Session not found")
    # Get tutor question (in a real app, you might want to track the current question)
    tutor_question = await call_agent_async(tutor_runner, user_id, session_id, answer)
    add_tutor_question(session_service, APP_NAME, user_id, session_id, tutor_question)
    add_user_answer(session_service, APP_NAME, user_id, session_id, answer)
    # Get feedback
    feedback = await call_agent_async(feedback_runner, user_id, session_id, answer)
    return {
        "tutor_question": tutor_question,
        "feedback": feedback
    }

@app.get("/session_state")
async def get_session_state(user_id: str, session_id: str):
    if user_id not in active_sessions or active_sessions[user_id].session_id != session_id:
        raise HTTPException(status_code=404, detail="Session not found")
    session = session_service.get_session(APP_NAME, user_id, session_id)
    return session.state