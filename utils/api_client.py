import requests

from requests import Response


class ApiClient:

    def __init__(self):
        self.url = 'http://127.0.0.1:5000'

    def get_home(self) -> Response:
        return requests.get(
            self.url
        )

    def post_create_store(self, name: str) -> Response:
        return requests.post(
            f'{self.url}/store/{name}'
        )

    def get_store(self, name: str) -> Response:
        return requests.get(
            f'{self.url}/store/{name}'
        )

    def get_stores(self) -> Response:
        return requests.get(
            f'{self.url}/store'
        )

    def post_create_item(self, store_name: str, body: dict = None) -> Response:
        return requests.post(
            f'{self.url}/store/{store_name}/item',
            json=body
        )

    def get_items(self, store_name: str) -> Response:
        return requests.get(
            f'{self.url}/store/{store_name}/item'
        )


api_client = ApiClient()
