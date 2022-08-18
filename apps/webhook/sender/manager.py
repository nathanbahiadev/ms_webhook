from threading import Thread

from django.conf import settings

from apps.webhook.models import Webhook
from apps.webhook.sender.consumer import WebhookSenderConsumer
from apps.webhook.sender.senders import WebhookSender


class WebhookSenderManager:
    def __init__(
        self,
        number_of_workers: int = settings.WORKERS,
        jobs_per_worker: int = settings.MAX_JOBS_PER_WORKER,
        user_id: int = None
    ):
        self.workers = {}
        self.number_of_workers = number_of_workers
        self.max_jobs_per_worker = jobs_per_worker
        self.user_id = user_id

    def main(self):
        jobs = self.split(self.filter())

        for worker in jobs:
            self.workers[worker] = Thread(self.execute, args=[jobs[worker]])

        [worker.start() for worker in self.workers.values()]
        [worker.join() for worker in self.workers.values()]

    def execute(self, webhooks):
        for webhook in webhooks:
            consumer = WebhookSenderConsumer(webhook, sender_class=WebhookSender)
            consumer.send()

    def filter(self):
        number_of_webhooks = self.number_of_workers * self.max_jobs_per_worker
        return Webhook.objects.filter(
            is_active=True,
            sended=False,
            failed=False
        ).order_by('created_at')[:number_of_webhooks]

    def split(self, webhooks):
        a_index, b_index, jobs = 0, self.max_jobs_per_worker, {}

        for i in range(1, self.number_of_workers + 1):
            jobs[f'worker-{i}'] = webhooks[a_index:b_index]
            a_index += self.max_jobs_per_worker
            b_index += self.max_jobs_per_worker

        return jobs
