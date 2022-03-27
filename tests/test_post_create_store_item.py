from utils.api_client import api_client
from utils.random_generator import generate_name, rand_float


def test_post_create_store_item_201():
    store_name = 'roman'
    data = {
        'name': generate_name(pref='auto_item_'),
        'price': rand_float()
    }

    response = api_client.post_create_item(store_name=store_name, body=data)

    assert response.status_code == 201
    assert response.json() == data

    response = api_client.get_items(store_name=store_name)
    assert response.status_code == 200
    response_data = response.json()
    assert data['name'] in [item['name'] for item in response_data['items']]
    assert data['price'] in [item['price'] for item in response_data['items']]


def test_post_create_store_item_404():
    name = generate_name()

    response = api_client.get_store(name=name)
    assert response.status_code == 404
    assert response.text == '"Store not found"\n'
