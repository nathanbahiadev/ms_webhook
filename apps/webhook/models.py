import json

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Webhook(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='webhooks', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    identifier = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    json_data = models.TextField(blank=True, null=True)
    sending_attempts = models.PositiveIntegerField(default=0)
    sended = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)
    return_from_receiver_text = models.TextField(blank=True, null=True)
    return_from_receiver_json = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'<Webhook: {self.user.username} #{self.identifier}>'

    @property
    def get_json_data(self):
        return json.loads(self.json_data or '{}')

    @property
    def get_return_from_receiver_json(self):
        return json.loads(self.return_from_receiver_json or '{}')

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
