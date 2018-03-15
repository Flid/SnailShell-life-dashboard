import json
from threading import Thread

from kivy.app import App
from kivy.logger import Logger as log
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin

from ..base import PluginBase


class Worker(ConsumerMixin):
    task_queue = Queue('tasks', Exchange('tasks'), 'tasks')

    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(
                queues=[self.task_queue],
                callbacks=[self.on_task],
            ),
        ]

    def on_task(self, body, message):
        try:
            log.info('Got task: {0!r}'.format(body))

            body = json.loads(body)

            command = body['command']

            if command == 'set_screen':
                App.get_running_app().sm.current = body['screen_name']
            else:
                raise ValueError('Unknown command %s', command)
        except Exception:
            log.exception('Error while processing request')
            return

        finally:
            # Even in case of an error we call `ack`. The message is incorrect,
            #  not the consumer. There's a very low chance it will
            # be processed next time.
            message.ack()


class Plugin(PluginBase):
    def after_load(self):
        rabbit_url = (
            f'amqp://{self.settings.RABBITMQ_USER}:'
            f'{self.settings.RABBITMQ_PASSWORD}@'
            f'{self.settings.MASTER_HOST}:'
            f'{self.settings.RABBITMQ_PORT}/'
        )
        conn = Connection(rabbit_url, heartbeat=10)
        worker = Worker(conn)

        self._worker_thread = Thread(target=worker.run)
        self._worker_thread.daemon = True
        self._worker_thread.start()
