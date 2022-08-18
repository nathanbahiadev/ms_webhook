from unittest.mock import patch

import pytest


@pytest.mark.django_db
def test_str_webhook(webhook):
    assert str(webhook) == f'<Webhook: {webhook.user.username} #{webhook.identifier}>'


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
