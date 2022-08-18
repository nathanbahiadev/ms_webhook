from unittest.mock import patch

import pytest
from requests.auth import HTTPBasicAuth

from apps.webhook.sender.senders import (
    WebhookSender,
    NoAuthenticatedSender,
    BasicAuthenticatedSender,
    JwtAuthenticatedSender,
    ApiKeyAuthenticatedSender
)


@pytest.mark.django_db
def test_create_sender_instance(webhook):
    sender = WebhookSender(webhook)
    assert sender.webhook == webhook


@pytest.mark.django_db
def test_create_no_auth_sender_instance(webhook):
    sender = NoAuthenticatedSender(webhook)
    assert sender.webhook == webhook


@pytest.mark.django_db
def test_create_basic_auth_sender_instance(webhook):
    sender = BasicAuthenticatedSender(webhook)
    assert sender.webhook == webhook


@pytest.mark.django_db
def test_create_jwt_auth_sender_instance(webhook):
    sender = JwtAuthenticatedSender(webhook)
    assert sender.webhook == webhook


@pytest.mark.django_db
def test_create_api_key_auth_sender_instance(webhook):
    sender = ApiKeyAuthenticatedSender(webhook)
    assert sender.webhook == webhook


@pytest.mark.django_db
def test_sender_no_authenticated_request(webhook):
    with patch('apps.webhook.sender.senders.requests') as mock_request:
        webhook.authentication = '0'
        WebhookSender(webhook).send()
        mock_request.request.assert_called_with(
            method=webhook.method,
            url=webhook.url,
            data=webhook.json_data,
            headers=webhook.headers
        )


@pytest.mark.django_db
def test_sender_basic_authenticated_request(webhook):
    with patch('apps.webhook.sender.senders.requests') as mock_request:
        webhook.authentication = '1'
        WebhookSender(webhook).send()
        mock_request.request.assert_called_with(
            method=webhook.method,
            url=webhook.url,
            data=webhook.json_data,
            headers=webhook.headers,
            auth=HTTPBasicAuth(
                webhook.auth_username,
                webhook.auth_password
            )
        )


@pytest.mark.django_db
def test_sender_api_key_authenticated_request(webhook):
    with patch('apps.webhook.sender.senders.requests') as mock_request:
        webhook.authentication = '3'
        WebhookSender(webhook).send()
        headers = {'HTTP_AUTHORIZATION': webhook.api_key}
        mock_request.request.assert_called_with(
            method=webhook.method,
            url=webhook.url,
            data=webhook.json_data,
            headers=headers,
        )


@pytest.mark.django_db
def test_sender_jwt_authenticated_request_raises_not_implementated_exception(webhook):
    with pytest.raises(Exception):
        webhook.authentication = '2'
        WebhookSender(webhook).send()
