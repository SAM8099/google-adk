from pydantic import BaseModel, Field
from typing import Optional, List

class User_answer(BaseModel):
    question_id: int
    answer: str = Field(..., description="The user's answer to the question.")