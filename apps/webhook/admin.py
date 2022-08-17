from django.contrib import admin

from apps.webhook import models


admin.site.register(models.Webhook)
admin.site.register(models.Errors)
