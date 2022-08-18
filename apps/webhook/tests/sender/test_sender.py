from unittest.mock import patch

import pytest
from requests.auth import HTTPBasicAuth

from apps.webhook.sender import Sender


@pytest.mark.django_db
def test_create_sender_instance(webhook):
    sender = Sender(webhook)
    assert sender.webhook == webhook


@pytest.mark.django_db
def test_sender_must_have_only_send_method(webhook):
    sender = Sender(webhook)
    valid_method_prefix = lambda method: method.startswith('__') is False and method.startswith('_Sender') is False
    methods_list = [method for method in dir(sender) if valid_method_prefix(method)]
    assert {'send', 'webhook'} == set(methods_list)
    assert len(methods_list) == 2


@pytest.mark.django_db
def test_sender_no_authenticated_request(webhook):
    with patch('apps.webhook.sender.requests') as mock_request:
        webhook.authentication = '0'
        Sender(webhook).send()
        mock_request.request.assert_called_with(
            method=webhook.method,
            url=webhook.url,
            data=webhook.json_data,
            headers=webhook.headers
        )


@pytest.mark.django_db
def test_sender_basic_authenticated_request(webhook):
    with patch('apps.webhook.sender.requests') as mock_request:
        webhook.authentication = '1'
        Sender(webhook).send()
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
    with patch('apps.webhook.sender.requests') as mock_request:
        webhook.authentication = '3'
        Sender(webhook).send()
        headers = {'HTTP_AUTHORIZATION': webhook.api_key}
        mock_request.request.assert_called_with(
            method=webhook.method,
            url=webhook.url,
            data=webhook.json_data,
            headers=headers,
        )


@pytest.mark.django_db
def test_sender_jwt_authenticated_request_raises_not_implementated_exception(webhook):
    with pytest.raises(NotImplementedError):
        webhook.authentication = '2'
        Sender(webhook).send()
