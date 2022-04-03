from tests.utils.api_client import api_client
from tests.utils.random_generator import generate_name


def test_put_update_item_200():
    name = generate_name()
    price = 99.99
    store_id = 1

    response = api_client.put_update_item(
        name=name,
        body={'price': price, 'store_id': store_id}
    )

    assert response.status_code == 200
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

    new_price = 11.11

    response = api_client.put_update_item(
        name=name,
        body={'price': new_price, 'store_id': 1}
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data['name'] == name
    assert response_data['price'] == new_price
    assert response_data['store_id'] == store_id

    response = api_client.get_item(name=name)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['name'] == name
    assert response_data['price'] == new_price
    assert response_data['store_id'] == store_id
