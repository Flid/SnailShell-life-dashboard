from threading import Thread

from kivy.logger import Logger as logger
from kombu import Connection, Exchange, Producer, Queue

from life_dashboard import settings

from ..base import PluginBase
from .camera import Camera


class Worker:
    task_queue = Queue(
        settings.PHOTO_CAPTURE_QUEUE_NAME,
        exchange=Exchange(settings.PHOTO_CAPTURE_QUEUE_NAME, type='direct'),
        routing_key=settings.PHOTO_CAPTURE_QUEUE_NAME,
        message_ttl=settings.PHOTO_CAPTURE_QUEUE_TTL,
    )

    def __init__(self, connection):
        self.connection = connection

    def run(self):
        while True:
            try:
                channel = self.connection.channel()

                producer = Producer(
                    exchange=self.task_queue.exchange,
                    channel=channel,
                    routing_key=settings.PHOTO_CAPTURE_QUEUE_NAME,
                    compression='bzip2',
                    serializer='raw',
                )
                self.task_queue.maybe_bind(self.connection)
                self.task_queue.declare()

                for photo in Camera().capture_continuous():
                    producer.publish(photo.tobytes())

            except Exception:
                logger.exception('Photo Capture error')


class Plugin(PluginBase):
    """
    This plugin connects to the camera and captures one image per second.
    The raw image will be sent to the master RabbitMQ.
    """
    def after_load(self):
        conn = Connection(settings.RABBTMQ_DSN)
        worker = Worker(conn)

        self._worker_thread = Thread(target=worker.run)
        self._worker_thread.daemon = True
        self._worker_thread.start()
