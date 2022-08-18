from uuid import uuid4

import pytest
from model_bakery import baker
from django.urls import reverse

from apps.webhook.models import Webhook


@pytest.mark.django_db
def test_delete_webhooks_must_return_204_when_delete_succeed(client, user):
    webhook = baker.make(Webhook, user=user)
    token = f'Token {user.auth_token.key}'
    url_delete_webhooks = reverse('webhook:delete_webhook', args=[webhook.id])
    response = client.delete(url_delete_webhooks, **{'HTTP_AUTHORIZATION': token})
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_webhooks_must_return_404_when_webhook_not_exists(client, user):
    token = f'Token {user.auth_token.key}'
    url_delete_webhooks = reverse('webhook:delete_webhook', args=[uuid4()])
    response = client.delete(url_delete_webhooks, **{'HTTP_AUTHORIZATION': token})
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_webhooks_must_return_404_when_user_is_not_the_webhooks_owner(client, user, webhook):
    token = f'Token {user.auth_token.key}'
    url_delete_webhooks = reverse('webhook:delete_webhook', args=[webhook.id])
    response = client.delete(url_delete_webhooks, **{'HTTP_AUTHORIZATION': token})
    assert response.status_code == 404
