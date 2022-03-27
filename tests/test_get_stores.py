from utils.api_client import api_client


def test_get_stores_200():
    name = 'roman'

    response = api_client.get_stores()
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) >= 1
    assert name in response_data
