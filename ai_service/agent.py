from google.adk.agents import Agent
import os


model = os.getenv("OLLAMA_MODEL")
# Agent initialized without instruction. TO BUILD
inventory_agent = Agent(
    name="inventory_agent",
    model=f"ollama_chat/{model}",
    instruction="""
You are an inventory agent.

For every user message, ignore the content of the question.
Always answer with exactly this sentence and nothing else:

I got your message, respond later!
"""
)