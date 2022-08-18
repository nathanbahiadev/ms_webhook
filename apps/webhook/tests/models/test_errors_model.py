import pytest


@pytest.mark.django_db
def test_str_error(error):
    assert str(error) == f'<Errors: {error.webhook_id} - {error.error_type} - {error.error_message}>'
