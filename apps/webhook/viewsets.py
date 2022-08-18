from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from apps.webhook.serializers import WebhookSerializer


@api_view(http_method_names=['POST'])
def create_webhook(request):
    serializer = WebhookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
