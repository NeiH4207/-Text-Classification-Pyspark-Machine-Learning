import pika
import json

from config import HOST, PORT, ROUTING_KEY, ES_INDEX
from elasticSearch.push_data import ElasticSearch

id = 1


def callback(channel, method, properties, body):
    """
    Receive message from queue and push message to elasticsearch
    """
    global id
    msg = json.loads(body)
    es = ElasticSearch()
    es.push_msg(
        index=ES_INDEX,
        id=id,
        msg=msg
    )
    id += 1
    # pop message out of queue
    channel.basic_ack(delivery_tag=method.delivery_tag)


def consume():
    """
    Subcribe to RabbitMQ queue to get message from queue
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST, port=PORT))
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=ROUTING_KEY,
        auto_ack=True,
        on_message_callback=callback
    )
    channel.start_consuming()
