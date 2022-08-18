import json
from unittest.mock import patch

import pytest
import requests.exceptions
import responses

from apps.webhook.sender.senders import BasicSender
from apps.webhook.sender.consumer import WebhookSenderConsumer


@pytest.fixture
def consumer(webhook):
    return WebhookSenderConsumer(webhook, sender_class=BasicSender)


@pytest.mark.django_db
def test_create_webhook_consumer_consumer_instance(consumer):
    assert consumer.Sender.__name__ == 'BasicSender'


@pytest.mark.django_db
def test_consumer_must_have_only_send_method(consumer):
    valid_method_prefix = lambda method: method.startswith('__') is False and method.startswith('_WebhookSenderConsumer') is False
    methods_list = [method for method in dir(consumer) if valid_method_prefix(method)]
    assert {'Sender', 'send', 'webhook'} == set(methods_list)
    assert len(methods_list) == 3


@pytest.mark.django_db
def test_consumer_send_with_successfully_no_authenticated_request(consumer):
    response_data = {'ok': True}
    responses.add(responses.Response(
        method="POST",
        url=consumer.webhook.url,
        status=200,
        json=response_data
    ))
    mock_consumer_send = responses.activate(consumer.send)
    mock_consumer_send()
    assert consumer.webhook.return_from_receiver_json == response_data
    assert consumer.webhook.return_from_receiver_text == json.dumps(response_data)
    assert consumer.webhook.sended is True


@pytest.mark.django_db
def test_consumer_send_with_failed_no_authenticated_request(consumer):
    responses.add(responses.Response(
        method="POST",
        url=consumer.webhook.url,
        status=400,
    ))
    mock_consumer_send = responses.activate(consumer.send)
    mock_consumer_send()
    assert consumer.webhook.return_from_receiver_json is None
    assert consumer.webhook.return_from_receiver_text is None
    assert consumer.webhook.sended is False
    logs = consumer.webhook.logs.all()
    assert logs.count() == 1
    assert logs.last().error_type == 'Exception'
    assert logs.last().status == 400


@pytest.mark.django_db
def test_consumer_send_with_exception_no_authenticated_request(consumer):
    with patch('apps.webhook.sender.senders.requests') as mock_requests:
        mock_requests.request.side_effect = requests.exceptions.ConnectionError('an unexpected error happened')
        consumer.send()
        assert consumer.webhook.return_from_receiver_json is None
        assert consumer.webhook.return_from_receiver_text is None
        assert consumer.webhook.sended is False
        logs = consumer.webhook.logs.all()
        assert logs.count() == 1
        assert logs.last().status is None
        assert logs.last().error_type == 'ConnectionError'
        assert logs.last().error_message == 'an unexpected error happened'
