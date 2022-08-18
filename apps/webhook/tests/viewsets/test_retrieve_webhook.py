from uuid import uuid4

import pytest
from model_bakery import baker
from django.urls import reverse

from apps.webhook.models import Webhook


@pytest.mark.django_db
def test_retrieve_webhooks_must_return_200_when_retrieve_succeed(client, user):
    webhook = baker.make(Webhook, user=user)
    token = f'Token {user.auth_token.key}'
    url_retrieve_webhooks = reverse('webhook:retrieve_webhook', args=[webhook.id])
    response = client.get(url_retrieve_webhooks, **{'HTTP_AUTHORIZATION': token})
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['user'] == user.email


@pytest.mark.django_db
def test_retrieve_webhooks_must_return_404_when_webhook_not_exists(client, user):
    token = f'Token {user.auth_token.key}'
    url_retrieve_webhooks = reverse('webhook:retrieve_webhook', args=[uuid4()])
    response = client.get(url_retrieve_webhooks, **{'HTTP_AUTHORIZATION': token})
    assert response.status_code == 404


@pytest.mark.django_db
def test_retrieve_webhooks_must_return_404_when_user_is_not_the_webhooks_owner(client, user, webhook):
    token = f'Token {user.auth_token.key}'
    url_retrieve_webhooks = reverse('webhook:retrieve_webhook', args=[webhook.id])
    response = client.get(url_retrieve_webhooks, **{'HTTP_AUTHORIZATION': token})
    assert response.status_code == 404
