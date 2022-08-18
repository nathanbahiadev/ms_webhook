import pytest
from django.urls import reverse


url_create_webhook = reverse('webhook:create_webhook')


@pytest.mark.django_db
def test_create_webhook_status_code_when_user_is_not_authenticated_must_be_401(client):
    response = client.get(url_create_webhook)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_webhook_status_code_when_user_is_not_authenticated_must_be_200(client, user):
    token = f'Token {user.auth_token.key}'
    response = client.get(url_create_webhook, **{'HTTP_AUTHORIZATION': token})
    assert response.status_code == 200
