import json
from unittest.mock import patch

import pytest
from model_bakery import baker

from apps.webhook.models import Webhook


@pytest.fixture()
@pytest.mark.django_db
def webhook():
    return baker.make(Webhook)


@pytest.mark.django_db
def test_str_webhook(webhook):
    assert str(webhook) == f'<Webhook: {webhook.user.username} #{webhook.identifier}>'


@pytest.mark.django_db
def test_get_json_data_webhook_must_be_none(webhook):
    assert isinstance(webhook.get_json_data, dict)
    assert webhook.get_json_data == {}


@pytest.mark.django_db
def test_get_return_from_receiver_json_must_be_none(webhook):
    assert isinstance(webhook.get_return_from_receiver_json, dict)
    assert webhook.get_return_from_receiver_json == {}


@pytest.mark.django_db
def test_get_json_data_webhook_must_a_dict():
    json_data = {'name': 'nathan', 'age': 28}
    webhook = baker.make(Webhook, json_data=json.dumps(json_data))
    assert isinstance(webhook.get_json_data, dict)
    assert isinstance(webhook.json_data, str)
    assert webhook.get_json_data == json_data


@pytest.mark.django_db
def test_get_return_from_receiver_json_must_be_a_dict():
    return_from_receiver_json = {'name': 'nathan', 'age': 28}
    webhook = baker.make(Webhook, return_from_receiver_json=json.dumps(return_from_receiver_json))
    assert isinstance(webhook.get_return_from_receiver_json, dict)
    assert isinstance(webhook.return_from_receiver_json, str)
    assert webhook.get_return_from_receiver_json == return_from_receiver_json


@pytest.mark.django_db
def test_increment_attempts_once(webhook):
    webhook.increment_attempts()
    with patch('apps.webhook.models.settings') as mock_settings:
        mock_settings.MAX_SENDING_ATTEMPTS = 2
        assert webhook.sending_attempts == 1
        assert webhook.is_active is True
        assert webhook.failed is False


@pytest.mark.django_db
def test_increment_attempts_twice(webhook):
    with patch('apps.webhook.models.settings') as mock_settings:
        mock_settings.MAX_SENDING_ATTEMPTS = 2
        webhook.increment_attempts()
        webhook.increment_attempts()
        assert webhook.sending_attempts == 2
        assert webhook.is_active is True
        assert webhook.failed is False


@pytest.mark.django_db
def test_exceeded_sending_attempts_failed_flag_must_be_activated(webhook):
    with patch('apps.webhook.models.settings') as mock_settings:
        mock_settings.MAX_SENDING_ATTEMPTS = 2
        webhook.increment_attempts()
        webhook.increment_attempts()
        webhook.increment_attempts()
        assert webhook.sending_attempts == 3
        assert webhook.is_active is False
        assert webhook.failed is True


@pytest.mark.django_db
def test_log_error(webhook):
    webhook.log_error(error=Exception('an error has occurred'))
    log = webhook.logs.first()
    assert log.status is None
    assert log.error_type == 'Exception'
    assert log.error_message == 'an error has occurred'
