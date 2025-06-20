from google.adk import Agent 

def create_feedback_agent():
    """Create and return the Feedback Agent."""
    return Agent(
    name="Feedback_Agent",
    model="gemini-2.0-flash",
    description="Provides feedback on the user's solution to a problem.",
    instruction="""
            Review the full conversation history (all events in the session) and the session state.
            **Content:**
            <content>
            {content}
            </content>
            **User's answers:**
            <user_answers>
            {user_answers}
            </user_answers>
            **Tutor's questions:**
            <tutor_questions>
            {tutor_questions}
            </tutor_questions>
            **Current Problem:**
            <current_problem>
            {current_problem}
            </current_problem>
            Use the session state to understand the user's current problem and their previous answers.
            Analyze the user's responses and the tutor's questions to determine if the user has demonstrated a complete understanding of the topic. 
            Pay special attention to the user's answers and the tutor's questions. 
            If the user demonstrates complete understanding of the topic, reply with 'exit' and nothing else. 
            Otherwise, reply with 'continue' and nothing else.
            """,
)