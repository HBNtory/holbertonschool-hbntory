from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from agent import inventory_agent

# Creation of service
session_service = InMemorySessionService()

# Creation of the runner
runner = Runner(
    agent=inventory_agent,
    app_name="hbntory",
    session_service=session_service,
)


async def run_inventory_agent(question: str) -> str:
    await session_service.create_session(
        app_name="hbntory",
        user_id="user",
        session_id="default",
    )

    try:
        events = runner.run_async(
            user_id="user",
            session_id="default",
            new_message=Content(
                role="user",
                parts=[Part(text=question)],
            ),
        )
        response = "No response."
        async for event in events:

            if event.content and event.content.parts:
                response = event.content.parts[-1].text

        return response

    finally:
        await session_service.delete_session(
            app_name="hbntory",
            user_id="user",
            session_id="default",
        )
