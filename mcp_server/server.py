from fastmcp import FastMCP
from config import PRODUCT_API_URL, BACKOFFICE_API_URL
import requests

mcp = FastMCP("Product MCP Server")


@mcp.tool
def list_products():
    """List all products."""
    response = requests.get(f"{PRODUCT_API_URL}/api/v1/products")

    status_code = response.status_code
    if status_code == 200:
        return response.json()

    return {"error": "Products not Found",
            "status_code": status_code,
            }


@mcp.tool
def get_product(id_or_sku: str):
    """Get a product by id or SKU."""
    response = requests.get(
        f"{PRODUCT_API_URL}/api/v1/products/{id_or_sku}"
    )
    status_code = response.status_code
    if status_code == 200:
        return response.json()

    return {"error": "Product not Found",
            "status_code": status_code,
    }



@mcp.tool
def get_stock_by_branch_label_and_product_id(branch_label: str,
                                             product_id: int) -> dict:
    """Get a stock by branch label and product ID."""
    url = f"{BACKOFFICE_API_URL}/stocks/{branch_label}/{product_id}"
    response = requests.get(url)

    status_code = response.status_code
    if status_code == 200:
        return response.json()

    return {"error": "Stock not Found",
            "status_code": status_code,
            }


if __name__ == "__main__":
    mcp.run(transport="streamable-http",
            host="0.0.0.0",
            port=6000)
