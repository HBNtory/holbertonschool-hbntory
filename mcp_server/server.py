from fastmcp import FastMCP
from config import PRODUCT_API_URL, BACKOFFICE_API_URL
import requests

mcp = FastMCP("Product MCP Server")


@mcp.tool
def get_product_by_id(id: int):
    """Get a product by id."""

    response = requests.get(
        f"{PRODUCT_API_URL}/api/v1/products/{id}"
    )
    status_code = response.status_code

    if status_code == 200:
        product = response.json()
        return {
            "id": product["id"],
            "sku": product["sku"],
            "name": product["name"],
        }

    return {
        "error": "Product not found",
        "status_code": status_code,
    }


@mcp.tool
def get_product_by_sku(sku: str):
    """Get a product by SKU."""

    response = requests.get(
        f"{PRODUCT_API_URL}/api/v1/products/{sku}"
    )
    status_code = response.status_code

    if status_code == 200:
        product = response.json()
        return {
            "id": product["id"],
            "sku": product["sku"],
            "name": product["name"],
        }

    return {
        "error": "Product not found",
        "status_code": status_code,
    }


@mcp.tool
def get_product_by_name(query: str):
    """Search products by name, SKU, description or tags."""

    response = requests.get(
        f"{PRODUCT_API_URL}/api/v1/products/search",
        params={"q": query},
    )

    if response.status_code == 200:
        return response.json()

    return {
        "error": "Products not found",
        "status_code": response.status_code,
    }


@mcp.tool
def get_stock_by_branch_label_and_product_id(branch_label: str,
                                             product_id: int):
    """Get stock for a product in a branch."""

    response = requests.get(
        f"{BACKOFFICE_API_URL}/stocks/{branch_label}/{product_id}"
    )
    status_code = response.status_code

    if status_code == 200:
        return response.json()

    return {
        "error": "Stock not found",
        "status_code": status_code,
    }


@mcp.tool
def get_available_products_by_branch(branch_label: str):
    """Get all available products in a branch."""

    response = requests.get(
        f"{BACKOFFICE_API_URL}/stocks/{branch_label}"
    )
    status_code = response.status_code

    if status_code == 200:
        products = []

        for stock in response.json():
            product_response = requests.get(
                f"{PRODUCT_API_URL}/api/v1/products/{stock['product_id']}"
            )

            if product_response.status_code != 200:
                continue

            product = product_response.json()

            products.append({
                "id": product["id"],
                "sku": product["sku"],
                "name": product["name"],
                "quantity": stock["quantity"],
            })

        return {
            "branch": branch_label,
            "products": products,
        }

    return {
        "error": "Branch not found",
        "status_code": status_code,
    }


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=6000,
    )
