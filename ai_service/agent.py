from google.adk.agents import Agent

# Agent initialized without instruction. TO BUILD
inventory_agent = Agent(
    name="inventory_agent",
    model="ollama_chat/qwen3:latest",
    instruction=""
)