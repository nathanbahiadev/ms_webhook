import pytest
from model_bakery import baker
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from apps.users.signals import create_token


@pytest.fixture
@pytest.mark.django_db
def user():
    return baker.make(get_user_model())


@pytest.mark.django_db
def test_create_token(user):
    token = Token.objects.filter(user=user).exists()
    assert token is True


@pytest.mark.django_db
def test_create_token_with_existing_user_must_not_create_another_token(user):
    token, created = create_token(sender=get_user_model(), instance=user)
    assert created is False
    assert Token.objects.get(key=token).user == user


@pytest.mark.django_db
def test_create_token_with_user_without_token_must_create_a_token(user):
    Token.objects.filter(user=user).delete()
    token, created = create_token(sender=get_user_model(), instance=user)
    assert created is True
    assert Token.objects.get(key=token).user == user
