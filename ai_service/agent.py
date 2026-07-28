from google.adk.agents import Agent
import os


model = os.getenv("OLLAMA_MODEL")
# Agent initialized without instruction. TO BUILD
inventory_agent = Agent(
    name="inventory_agent",
    model=f"ollama_chat/{model}",
    instruction="You are an inventory agent."
                "for now, you ALWAYS respond this sentence:"
                "'I got your message, respond later !'"

)