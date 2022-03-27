from utils.api_client import api_client
from utils.random_generator import generate_name


def test_get_store_items_200():
    store_name = 'roman'
    data = {
        'name': 'lambo',
        'price': 500.0
    }

    response = api_client.get_items(store_name=store_name)
    assert response.status_code == 200
    response_data = response.json()
    assert data['name'] in [item['name'] for item in response_data['items']]
    assert data['price'] in [item['price'] for item in response_data['items']]


def test_get_store_items_404():
    name = generate_name()

    response = api_client.get_store(name=name)
    assert response.status_code == 404
    assert response.text == '"Store not found"\n'
