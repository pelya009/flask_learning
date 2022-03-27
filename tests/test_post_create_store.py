from utils.api_client import api_client
from utils.random_generator import generate_name


def test_post_create_store_201():
    name = generate_name()
    exp_response = {
        'name': name,
        'items': []
    }

    response = api_client.post_create_store(name=name)

    assert response.status_code == 201
    assert response.json() == exp_response

    response = api_client.get_store(name=name)
    assert response.status_code == 200
    assert response.json() == exp_response
