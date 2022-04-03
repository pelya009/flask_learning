from tests.utils.api_client import api_client
from tests.utils.random_generator import generate_name


def test_get_item_200():
    name = 'lambo'
    price = 500.0

    response = api_client.get_item(name=name)
    assert response.status_code == 200
    response_data = response.json()
    assert name == response_data['name']
    assert price == response_data['price']


def test_get_item_404():
    name = generate_name()

    response = api_client.get_item(name=name)
    assert response.status_code == 404
    assert response.json()['message'] == f'Item with name: "{name}" not found'
