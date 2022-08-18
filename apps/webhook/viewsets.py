from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from django.conf import settings

from apps.webhook.serializers import WebhookSerializer, WebhookListSerializer
from apps.webhook.models import Webhook


@api_view(['POST'])
def create_webhook(request):
    serializer = WebhookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_webhooks(request):
    paginator = PageNumberPagination()
    paginator.page_size = settings.PAGINATOR
    webhook_objects = Webhook.objects.filter(user=request.user, is_active=True).order_by('-created_at')
    result_page = paginator.paginate_queryset(webhook_objects, request)
    serializer = WebhookListSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def retrieve_webhook(request, webhook_id):
    webhook = get_object_or_404(Webhook, id=webhook_id, user=request.user, is_active=True)
    serializer = WebhookSerializer(webhook)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_webhook(request, webhook_id):
    webhook = get_object_or_404(Webhook, id=webhook_id, user=request.user, is_active=True)
    webhook.is_active = False
    webhook.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
