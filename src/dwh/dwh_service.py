from typing import Any

import pika
import json

from UUIDEncoder import UUIDEncoder
from action_dwh_enum import ActionDWHEnum
from cfg.сonfig import settings
from src.dwh.dwh_message import DwhMessage

class DwhService:

    QUEUE_NAME = 'dwh_queue'
    @staticmethod
    def send(object_type, object: Any, action: ActionDWHEnum, description: str):
        sending_message = DwhMessage(object_type,
                          object,
                          description,
                          action)
        DwhService.send_message(DwhService.QUEUE_NAME, sending_message.to_dict())

    @staticmethod
    def send_message(queue_name: str, message: dict):
        connection = pika.BlockingConnection(pika.ConnectionParameters(settings.get_MQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message, cls=UUIDEncoder))
        print(f" [x] Sent message to {queue_name}")
        connection.close()

def main():
    pass

if __name__ == '__main__':
    main()