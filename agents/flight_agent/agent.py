from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

flight_agent = Agent(
    name="flight_agent",
    model=LiteLlm("deepseek/deepseek-chat"),
    description="Suggests flight options for a destination.",
    instruction=(
        "Given a destination, travel dates, and budget, suggest 1-2 realistic flight options. "
        "Include airline name, price, and departure time. Ensure flights fit within the budget."
    )
)

session_service = InMemorySessionService()
runner = Runner(
    agent=flight_agent,
    app_name="flight_app",
    session_service=session_service
)

USER_ID = "user_1"
SESSION_ID = "session_001"

async def execute(request):
    # 🔧 Ensure session is created before running the agent
    await session_service.create_session(
        app_name="flight_app",
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    # prompt = (
    #     f"User is flying to {request['destination']} from {request['start_date']} to {request['end_date']}, "
    #     f"with a budget of {request['budget']}. Suggest flight options."
    # )
    prompt = (
    f"User is flying from {request['origin']} to {request['destination']} "
    f"from {request['start_date']} to {request['end_date']}, with a budget of {request['budget']}. "
    "Suggest 2-3 realistic flight options. For each option, include airline, departure time, return time, "
    "price, and mention if it's direct or has layovers."
    )


    message = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=message):
        if event.is_final_response():
            return {"flights": event.content.parts[0].text}
