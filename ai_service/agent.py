from google.adk.agents import Agent
import os


model = os.getenv("OLLAMA_MODEL")
# Agent initialized without instruction. TO BUILD
inventory_agent = Agent(
    name="inventory_agent",
    model="ollama_chat/qwen3:latest",
    instruction=""
)