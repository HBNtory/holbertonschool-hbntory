# Get the MCP server url
import os
# Create a fastmcp client
from fastmcp import Client


MCP_SERVER_URL = os.getenv("MCP_SERVER_URL")
client = Client(MCP_SERVER_URL)