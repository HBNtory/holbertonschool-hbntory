from google.adk.agents import Agent

inventory_agent = Agent(
    name="inventory_agent",
    model="ollama_chat/qwen3:latest",
    instruction="""
    You are an inventory assistant.
    """
)