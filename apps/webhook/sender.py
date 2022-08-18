import requests
from requests.auth import HTTPBasicAuth

from apps.webhook.models import Webhook


class WebhookSenderConsumer:
    def __init__(self, webhook: Webhook, sender_class):
        self.webhook = webhook
        self.Sender = sender_class

    def send(self):
        try:
            response = self.Sender(self.webhook).send()

            if response.ok or response.status_code == 200:
                self.webhook.return_from_receiver_json = response.json()
                self.webhook.return_from_receiver_text = response.text
                self.webhook.sended = True
                self.webhook.save()
                return

            self.webhook.log_error(status=response.status_code, error=Exception(response.text))

        except Exception as e:
            self.webhook.log_error(error=e)


class Sender:
    def __init__(self, webhook: Webhook):
        self.webhook = webhook

    def send(self):
        return {
            '0': self.__no_authenticated_request,
            '1': self.__basic_authenticated_request,
            '2': self.__jwt_authenticated_request,
            '3': self.__api_key_authenticated_request,
        }.get(self.webhook.authentication)()

    def __no_authenticated_request(self):
        return requests.request(
            method=self.webhook.method,
            url=self.webhook.url,
            data=self.webhook.json_data,
            headers=self.webhook.headers
        )

    def __basic_authenticated_request(self):
        auth = HTTPBasicAuth(self.webhook.auth_username, self.webhook.auth_password)
        return requests.request(
            method=self.webhook.method,
            url=self.webhook.url,
            data=self.webhook.json_data,
            headers=self.webhook.headers,
            auth=auth
        )

    def __jwt_authenticated_request(self):
        raise NotImplementedError

    def __api_key_authenticated_request(self):
        headers = self.webhook.headers or {}
        headers.update({'HTTP_AUTHORIZATION': self.webhook.api_key})
        return requests.request(
            method=self.webhook.method,
            url=self.webhook.url,
            data=self.webhook.json_data,
            headers=headers,
        )
