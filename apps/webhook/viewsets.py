from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(http_method_names=['GET'])
def create_webhook(request):
    return Response({'ok': True}, status=status.HTTP_200_OK)
