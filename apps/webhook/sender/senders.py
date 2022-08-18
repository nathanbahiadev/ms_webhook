import requests
from requests.auth import HTTPBasicAuth

from apps.webhook.models import Webhook


class NoAuthenticatedSender:
    def __init__(self, webhook: Webhook):
        self.webhook = webhook

    def no_auth_send(self):
        return requests.request(
            method=self.webhook.method,
            url=self.webhook.url,
            data=self.webhook.json_data,
            headers=self.webhook.headers
        )


class BasicAuthenticatedSender:
    def __init__(self, webhook: Webhook):
        self.webhook = webhook

    def basic_auth_send(self):
        auth = HTTPBasicAuth(self.webhook.auth_username, self.webhook.auth_password)
        return requests.request(
            method=self.webhook.method,
            url=self.webhook.url,
            data=self.webhook.json_data,
            headers=self.webhook.headers,
            auth=auth
        )


class ApiKeyAuthenticatedSender:
    def __init__(self, webhook: Webhook):
        self.webhook = webhook

    def api_key_auth_send(self):
        headers = self.webhook.headers or {}
        headers.update({'HTTP_AUTHORIZATION': self.webhook.api_key})
        return requests.request(
            method=self.webhook.method,
            url=self.webhook.url,
            data=self.webhook.json_data,
            headers=headers,
        )


class JwtAuthenticatedSender:
    def __init__(self, webhook: Webhook):
        self.webhook = webhook

    def jwt_auth_send(self):
        raise Exception('Not implemented')


class WebhookSender(
    NoAuthenticatedSender,
    BasicAuthenticatedSender,
    JwtAuthenticatedSender,
    ApiKeyAuthenticatedSender
):
    def __init__(self, webhook: Webhook):
        super().__init__(webhook)

    def send(self):
        return {
            '0': self.no_auth_send,
            '1': self.basic_auth_send,
            '2': self.jwt_auth_send,
            '3': self.api_key_auth_send,
        }.get(self.webhook.authentication)()
