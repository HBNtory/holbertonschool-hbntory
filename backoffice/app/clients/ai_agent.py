import os
import requests

AGENT_URL = os.getenv("AI_AGENT_URL")


def send_to_ai_agent(query: str) -> dict:
    """send the user query body to the ai agent"""
    response = requests.post(
        f"{AGENT_URL}/query",
        json={"query": query},
        timeout = 30
    )
    response.raise_for_status()
    return response.json()
