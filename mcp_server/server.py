from fastmcp import FastMCP

mcp = FastMCP("Product MCP Server")

if __name__ == "__main__":
    mcp.run( transport="streamable-http",
    host="0.0.0.0",
    port=6000)