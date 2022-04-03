from tests.utils.api_client import api_client
from tests.utils.random_generator import generate_name


def test_post_create_item_201():
    name = generate_name()
    price = 99.99
    store_id = 1

    response = api_client.post_create_item(
        name=name,
        body={'price': price, 'store_id': store_id}
    )

    assert response.status_code == 201
    response_data = response.json()
    assert response_data['name'] == name
    assert response_data['price'] == price
    assert response_data['store_id'] == store_id

    response = api_client.get_item(name=name)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['name'] == name
    assert response_data['price'] == price
    assert response_data['store_id'] == store_id
