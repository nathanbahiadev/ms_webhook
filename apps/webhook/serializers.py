from rest_framework import serializers

from apps.webhook.models import Webhook


class WebhookSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Webhook
        fields = '__all__'

        extra_kwargs = {
            'json_data': {'required': True},
            'user': {'read_only': True},
        }
