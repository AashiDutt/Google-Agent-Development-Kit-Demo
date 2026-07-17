from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

stay_agent = Agent(
    name="stay_agent",
    model=LiteLlm("deepseek/deepseek-chat"),
    description="Suggests hotel or stay options for a destination.",
    instruction=(
        "Given a destination, travel dates, and budget, suggest 2-3 hotel or stay options. "
        "Include hotel name, price per night, and location. Ensure suggestions are within budget."
    )
)

session_service = InMemorySessionService()
runner = Runner(
    agent=stay_agent,
    app_name="stay_app",
    session_service=session_service
)

USER_ID = "user_stay"
SESSION_ID = "session_stay"

async def execute(request):
    await session_service.create_session(
        app_name="stay_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    prompt = (
        f"User is staying in {request['destination']} from {request['start_date']} to {request['end_date']} "
        f"with a budget of {request['budget']}. Suggest stay options."
    )

    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            return {"stays": event.content.parts[0].text}
