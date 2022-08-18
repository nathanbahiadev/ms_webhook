from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=get_user_model())
def create_token(sender, instance, **kwargs):
    return Token.objects.get_or_create(user=instance)
