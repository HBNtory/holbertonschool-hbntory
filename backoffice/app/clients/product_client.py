import requests

from app.config import Config


class ProductClient:
    """Client fir the external Product API."""

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or Config.PRODUCT_API_URL

    def exists(self, product_id: int) -> bool:
        """Check whether a product exists in the Product API.

        Returns:
            True if the product exists (HTTP 200), False if not found (404).
        """
        url = f"{self.base_url}/api/v1/products/{product_id}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        response.raise_for_status()
        return False
