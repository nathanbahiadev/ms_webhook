import json

import pytest
from django.urls import reverse


url_create_webhook = reverse('webhook:create_webhook')

invalid_data = {}
valid_data = {
    'url': 'https://example.com',
    'json_data': json.dumps({'test': True})
}


@pytest.mark.django_db
def test_create_webhook_status_code_when_user_is_not_authenticated_must_be_401(client):
    response = client.post(url_create_webhook)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_webhook_status_code_when_user_is_not_authenticated_must_be_201_and_valid_data(client, user):
    token = f'Token {user.auth_token.key}'
    response = client.post(url_create_webhook, data=valid_data, **{'HTTP_AUTHORIZATION': token})
    response_json = response.json()
    assert response.status_code == 201
    assert response_json['user'] == user.email
    assert response_json['url'] == valid_data['url']
    assert response_json['json_data'] == json.loads(valid_data['json_data'])


@pytest.mark.django_db
def test_create_webhook_status_code_when_user_is_not_authenticated_must_be_400_and_invalid_data(client, user):
    token = f'Token {user.auth_token.key}'
    response = client.post(url_create_webhook, data=invalid_data, **{'HTTP_AUTHORIZATION': token})
    response_json = response.json()
    assert response.status_code == 400
    assert 'id' not in response_json
    assert 'user' not in response_json
