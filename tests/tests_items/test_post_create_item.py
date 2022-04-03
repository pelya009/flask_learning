from tests.utils.api_client import api_client
from tests.utils.random_generator import generate_name


def test_post_create_item_201():
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
    assert response.json() == exp_response

    response = api_client.get_item(name=name)
    assert response.status_code == 200
    assert response.json() == exp_response
