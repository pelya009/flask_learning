from utils.api_client import api_client
from utils.random_generator import generate_name


def test_get_store_200():
    name = 'roman'

    response = api_client.get_store(name=name)
    assert response.status_code == 200
    response_data = response.json()
    assert name == response_data['name']


def test_get_store_404():
    name = generate_name()

    response = api_client.get_store(name=name)
    assert response.status_code == 404
    assert response.text == '"Store not found"\n'
