import requests

from requests import Response


class ApiClient:

    def __init__(self):
        self.url = 'http://127.0.0.1:5000'

    def _get_token_header(self):
        token = self.get_access_token().json()['access_token']
        return {'Authorization': f'JWT {token}'}

    def get_home(self) -> Response:
        return requests.get(
            self.url
        )

    def get_access_token(self, username: str = 'admin', password: str = 'admin'):
        return requests.post(
            f'{self.url}/login',
            json={
                "username": username,
                "password": password
            }
        )

    def register(self, username: str = 'admin', password: str = 'admin'):
        return requests.post(
            f'{self.url}/register',
            json={
                "username": username,
                "password": password
            }
        )

    def get_items(self) -> Response:
        return requests.get(
            f'{self.url}/items'
        )

    def get_item(self, name: str) -> Response:
        return requests.get(
            f'{self.url}/item/{name}'
        )

    def post_create_item(self, name: str = None, body: dict = None) -> Response:
        headers = self._get_token_header()
        return requests.post(
            f'{self.url}/item/{name}',
            headers=headers,
            json=body
        )

    def put_update_item(self, name: str = None, body: dict = None) -> Response:
        headers = self._get_token_header()
        return requests.put(
            f'{self.url}/item/{name}',
            headers=headers,
            json=body
        )

    def delete_item(self, name: str = None) -> Response:
        headers = self._get_token_header()
        return requests.delete(
            f'{self.url}/item/{name}',
            headers=headers
        )


api_client = ApiClient()
