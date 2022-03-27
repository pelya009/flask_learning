from utils.api_client import api_client


def test_get_home_200():
    response = api_client.get_home()

    assert response.status_code == 200
    assert response.text == 'Hello, world!'
