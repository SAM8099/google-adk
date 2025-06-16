from google.genai import types

async def process_agent_response(event):
    """Process an agent event to extract the response text."""
    if event.content and event.content.parts:
        # Extract text from the first part (assuming parts is a list of Part objects)
        return event.content.parts[0].text
    return None


async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent asynchronously with the user's query."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = None

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):

            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f"{e}")

    return final_response_text