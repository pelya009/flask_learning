from tests.utils.api_client import api_client


def test_get_stores_200():
    data = {
        'name': 'italian_auto'
    }

    response = api_client.get_stores()
    assert response.status_code == 200
    response_data = response.json()
    assert data['name'] in [item['name'] for item in response_data]
