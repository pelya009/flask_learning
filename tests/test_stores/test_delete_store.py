from tests.utils.api_client import api_client
from tests.utils.random_generator import generate_name


def test_delete_store_200():
    name = generate_name()

    response = api_client.post_create_store(name=name)
    assert response.status_code == 201

    response = api_client.delete_store(name=name)
    assert response.status_code == 200


def test_delete_store_404():
    name = generate_name()

    response = api_client.delete_store(name=name)
    assert response.status_code == 404
    assert response.json()['message'] == f'Store with name: "{name}" not found'
