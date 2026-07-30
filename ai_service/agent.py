from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StreamableHTTPConnectionParams,
)
from services.prompt import prompt

mcp_server_url = os.environ.get("MCP_SERVER_URL")
model = os.getenv("OLLAMA_MODEL")

inventory_agent = Agent(
    name="inventory_agent",
    model=f"ollama_chat/{model}",
    instruction=prompt,
    tools=[
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=mcp_server_url,
            ),
        ),
    ],
)