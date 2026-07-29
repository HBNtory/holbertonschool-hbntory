from fastmcp import FastMCP
from config import PRODUCT_API_URL
import requests

mcp = FastMCP("Product MCP Server")


@mcp.tool
def list_products():
    """List all products."""
    response = requests.get(f"{PRODUCT_API_URL}/api/v1/products")

    if response.status_code == 200:
        return response.json()

    return response.json()


@mcp.tool
def get_product(id_or_sku: str):
    """Get a product by id or SKU."""
    response = requests.get(
        f"{PRODUCT_API_URL}/api/v1/products/{id_or_sku}"
    )

    if response.status_code == 200:
        return response.json()

    return response.json()


if __name__ == "__main__":
    mcp.run(transport="streamable-http",
            host="0.0.0.0",
            port=6000)
