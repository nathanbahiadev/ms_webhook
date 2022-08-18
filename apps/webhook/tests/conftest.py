import pytest
from model_bakery import baker

from apps.webhook.models import Webhook, Errors


@pytest.fixture
@pytest.mark.django_db
def error():
    return baker.make(Errors)


@pytest.fixture()
@pytest.mark.django_db
def webhook():
    return baker.make(Webhook)
