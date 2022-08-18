from django.urls import path

from apps.webhook import viewsets


app_name = 'webhook'

urlpatterns = [
    path('', viewsets.create_webhook, name='create_webhook'),
    path('list', viewsets.list_webhooks, name='list_webhooks'),
    path('<uuid:webhook_id>', viewsets.retrieve_webhook, name='retrieve_webhook'),
    path('<uuid:webhook_id>/delete/', viewsets.delete_webhook, name='delete_webhook'),
]
