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
