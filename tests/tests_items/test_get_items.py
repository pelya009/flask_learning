from tests.utils.api_client import api_client


def test_get_items_200():
    name = 'lambo'
    price = 500.0

    response = api_client.get_items()
    assert response.status_code == 200
    response_data = response.json()
    assert name in [item['name'] for item in response_data]
    assert price in [item['price'] for item in response_data]
