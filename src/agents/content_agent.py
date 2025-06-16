from google.adk import Agent

content_agent = Agent(
    name="Content Agent",
    model="gemini-2.0-flash",
    description="Generates content based on the provided context.",
    instructions="Provide a concise hint or definition, but do NOT solve the problem."
)