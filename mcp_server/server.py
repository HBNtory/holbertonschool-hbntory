from fastmcp import FastMCP
from config import PRODUCT_API_URL, BACKOFFICE_API_URL
import requests

mcp = FastMCP("Product MCP Server")


@mcp.tool
def get_product_by_id(id: int):
    """
    Retrieve a single product using its unique numeric ID.

    Use this tool when the user explicitly provides a product ID.
    Returns the product identifier, SKU and name.
    """

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
    """
    Retrieve a single product using its SKU.

    Use this tool when the user provides an exact SKU.
    Returns the product identifier, SKU and name.
    """

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
    """
    Search the product catalog by keyword.

    Use this tool when the user provides a product name,
    a partial name, a SKU fragment, a description keyword
    or a tag.

    Returns a list of matching products.
    """

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
    """
    Retrieve the stock quantity of a specific product
    in a specific branch.

    Use this tool when both the branch and the product
    are known.

    Returns the stock information for that product only.
    """

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
    """
    Retrieve all products available in a branch.

    Use this tool when the user asks which products
    are available in a given branch or wants the
    branch inventory.

    Returns a list of products with their quantity.
    """

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
