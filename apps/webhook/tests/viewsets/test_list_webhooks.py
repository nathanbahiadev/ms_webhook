import pytest
from model_bakery import baker
from django.urls import reverse

from apps.webhook.models import Webhook


url_list_webhooks = reverse('webhook:list_webhooks')


@pytest.mark.django_db
def test_list_webhooks_must_return_an_empty_list_when_there_is_no_webhooks_created(client, user):
    token = f'Token {user.auth_token.key}'
    response = client.get(url_list_webhooks, **{'HTTP_AUTHORIZATION': token})
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['count'] == 0


@pytest.mark.django_db
def test_list_webhooks_must_return_3_itens_when_there_is_3_webhooks_created_from_current_user(client, user):
    baker.make(Webhook, 3, user=user)
    token = f'Token {user.auth_token.key}'
    response = client.get(url_list_webhooks, **{'HTTP_AUTHORIZATION': token})
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['count'] == 3


@pytest.mark.django_db
def test_list_webhooks_must_return_0_itens_when_current_user_has_no_created_any(client, user):
    baker.make(Webhook, 3)
    token = f'Token {user.auth_token.key}'
    response = client.get(url_list_webhooks, **{'HTTP_AUTHORIZATION': token})
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['count'] == 0
