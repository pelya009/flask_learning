from tests.utils.api_client import api_client
from tests.utils.random_generator import generate_name


def test_delete_item_200():
    name = generate_name()
    exp_response = {
        'name': name,
        'price': 99.99
    }

    response = api_client.post_create_item(
        name=exp_response['name'],
        body={'price': exp_response['price'], 'store_id': 1}
    )
    assert response.status_code == 201

    response = api_client.delete_item(name=name)
    assert response.status_code == 200


def test_delete_item_404():
    name = generate_name()

    response = api_client.delete_item(name=name)
    assert response.status_code == 404
    assert response.json()['message'] == f'Item with name: "{name}" not found'
