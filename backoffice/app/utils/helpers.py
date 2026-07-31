import requests

from app.clients.product_client import ProductClient


def product_names() -> dict[int, str] | None:
    """Return a {product_id: name} map from the product catalog.

    Returns None if the catalog can't be fetched (API down/slow), so
    the caller can degrade gracefully instead of crashing.
    """
    try:
        catalog = ProductClient().list()
    except requests.RequestException:
        return None
    return {product["id"]: product["name"] for product in catalog}


def catalog_or_empty() -> list[dict]:
    """Return the product catalog, or an empty list if the API is down."""
    try:
        return ProductClient().list()
    except requests.RequestException:
        return []
