from tests.utils.api_client import api_client
from tests.utils.random_generator import generate_name


def test_register_200():
    username = generate_name()
    password = generate_name()

    response = api_client.register(username=username, password=password)
    assert response.status_code == 201

    response = api_client.get_access_token(username=username, password=password)
    assert response.status_code == 200
    assert response.json().get('access_token')
