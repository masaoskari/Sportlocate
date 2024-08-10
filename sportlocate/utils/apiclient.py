import requests
from retry import retry


class ApiClient:
    """
    A simple API client for making HTTP requests.
    """

    def __init__(self, base_url):
        """
        Initialize the ApiClient with a base URL.

        Args:
            base_url (str): The base URL for the API.
        """
        self.base_url = base_url

    @retry(tries=3, delay=2)  # Retry up to 3 times, waiting 2 seconds between retries
    def get(self, endpoint, params=None) -> dict:
        """
        Send a GET request to the specified endpoint.

        Args:
            endpoint (str): The endpoint to send the GET request to.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            dict: The JSON response from the server.

        Raises:
            requests.HTTPError: If the request results in an HTTP error.
        """
        response = requests.get(self.base_url + endpoint, params=params)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        return response.json()
