import pytest
from model_bakery import baker

from apps.webhook.models import Errors


@pytest.fixture
@pytest.mark.django_db
def error():
    return baker.make(Errors)


@pytest.mark.django_db
def test_str_error(error):
    assert str(error) == f'<Errors: {error.webhook_id} - {error.error_type} - {error.error_message}>'
