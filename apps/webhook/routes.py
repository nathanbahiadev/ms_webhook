from django.urls import path

from apps.webhook import viewsets


app_name = 'webhook'

urlpatterns = [
    path('', viewsets.create_webhook, name='create_webhook'),
]
