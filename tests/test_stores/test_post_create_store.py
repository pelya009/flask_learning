from tests.utils.api_client import api_client
from tests.utils.random_generator import generate_name


def test_post_create_store_201():
    name = generate_name()

    response = api_client.post_create_store(name=name)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data['name'] == name
    assert response_data['items'] == []
    assert response_data['id']

    response = api_client.get_store(name=name)
    response_data = response.json()
    assert response_data['name'] == name
    assert response_data['items'] == []
    assert response_data['id']
