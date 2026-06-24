import traceback
from fastapi import FastAPI, Response
import uvicorn

def create_app(agent):
    app = FastAPI()

    @app.post("/run")
    async def run(payload: dict):
        try:
            return await agent.execute(payload)
        except Exception as e:
            traceback.print_exc()
            return Response(
                content=f"Agent error: {type(e).__name__}: {e}",
                status_code=500
            )

    return app
