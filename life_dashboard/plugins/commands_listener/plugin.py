#from kombu import Connection, Exchange, Queue, Consumer
import socket

from kivy.app import App

from ..base import PluginBase


class Plugin(PluginBase):
    def after_load(self):
        return
        rabbit_url = (
            f'amqp://{self.settings.RABBITMQ_USER}:'
            f'{self.settings.RABBITMQ_PASSWORD}@'
            f'{self.settings.MASTER_HOST}:'
            f'{self.settings.RABBITMQ_PORT}/'
        )
        self._conn = Connection(rabbit_url, heartbeat=10)

        exchange = Exchange('example-exchange', type='direct')
        queue = Queue(
            name='example-queue', exchange=exchange,
            routing_key='BOB',
        )

        self._consumer = Consumer(
            self._conn,
            queues=queue,
            callbacks=[self._process_message],
            accept=['text/plain'],
        )
        self._consumer.consume()

        self.run()

    def _process_message(self, body, message):
        print('The body is {}'.format(body))
        message.ack()

    def _establish_connection(self):
        revived_connection = self._conn.clone()
        revived_connection.ensure_connection(max_retries=3)
        channel = revived_connection.channel()
        self._consumer.revive(channel)
        self._consumer.consume()
        return revived_connection

    def consume(self):
        new_conn = self._establish_connection()
        while True:
            try:
                new_conn.drain_events(timeout=2)
            except socket.timeout:
                new_conn.heartbeat_check()

    def run(self):
        while True:
            try:
                self._consume()
            except self._conn.connection_errors:
                print('connection revived')
