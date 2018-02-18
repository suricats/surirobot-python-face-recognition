import os
from threading import Thread


class RedisThread(Thread):
    def __init__(self, conn, name):
        Thread.__init__(self)
        self.conn = conn
        self.name = name

    def run(self):
        self.conn.publish(os.environ.get('FACERECO_REDIS_MODULE_NAME', 'face-recognition'), self.name)
