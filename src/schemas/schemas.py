from typing import Dict, List, Optional, Any
from pydantic import BaseModel

class SessionInfo(BaseModel):
    """Represents a user session in the backend."""
    user_id: str
    session_id: str

initial_state: Dict[str, Any] = {
    "user_name": "User 1",
    "current_problem": None,
    "tutor_questions": [],
    "user_answers": [],
    "content": None,
}

class QuestionRequest(BaseModel):
    user_id: str
    session_id: str

class ProblemRequest(BaseModel):
    user_id: str
    session_id: str
    problem: str
    
class UserAnswerRequest(BaseModel):
    user_id: str
    session_id: str
    answer: str