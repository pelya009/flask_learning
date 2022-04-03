from tests.utils.api_client import api_client
from tests.utils.random_generator import generate_name


def test_delete_user_200():
    username = generate_name()
    password = generate_name()

    response = api_client.register(username=username, password=password)
    assert response.status_code == 201
    user_id = response.json()['id']

    response = api_client.get_access_token(username=username, password=password)
    assert response.status_code == 200
    assert response.json().get('access_token')

    response = api_client.delete_user(user_id=user_id, username=username, password=password)
    assert response.status_code == 403
    assert response.text == '"You need admin permissions"\n'

    response = api_client.delete_user(user_id=user_id, username='admin', password='admin')
    assert response.status_code == 200
