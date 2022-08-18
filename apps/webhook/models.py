import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from apps.webhook.choices import AUTH_OPTIONS


class Webhook(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='webhooks', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    identifier = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    sending_attempts = models.PositiveIntegerField(default=0)
    sended = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)
    return_from_receiver_text = models.TextField(blank=True, null=True)
    return_from_receiver_json = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    url = models.URLField()
    method = models.CharField(max_length=255, default='post')
    json_data = models.JSONField(blank=True, null=True)
    authentication = models.CharField(max_length=1, default='0', choices=AUTH_OPTIONS)
    auth_username = models.CharField(max_length=255, blank=True, null=True)
    auth_password = models.CharField(max_length=255, blank=True, null=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    url_token = models.URLField(blank=True, null=True)
    headers = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'<Webhook: {self.user.username} #{self.identifier}>'

    def log_error(self, error: Exception, status: int = None):
        self.increment_attempts()
        Errors.objects.create(
            webhook=self,
            status=status,
            error_type=error.__class__.__name__,
            error_message=str(error)
        )

    def increment_attempts(self):
        self.sending_attempts += 1
        if settings.MAX_SENDING_ATTEMPTS < self.sending_attempts:
            self.failed = True
            self.is_active = False
        self.save()


class Errors(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    webhook = models.ForeignKey(Webhook, on_delete=models.PROTECT, related_name='logs')
    status = models.PositiveIntegerField(blank=True, null=True)
    error_type = models.CharField(max_length=255, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'<Errors: {self.webhook_id} - {self.error_type} - {self.error_message}>'
