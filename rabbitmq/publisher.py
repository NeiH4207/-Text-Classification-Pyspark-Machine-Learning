import pika

from config import HOST, PORT, EXCHANGE, ROUTING_KEY


def publish(msg):
    """
        Publish message to RabbitMQ queue
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST, port=PORT))
    channel = connection.channel()
    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=ROUTING_KEY,
        body=msg,
        delivery_mode=2)
    channel.close()
