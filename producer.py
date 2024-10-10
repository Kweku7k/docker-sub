import pika, json

connection = pika.BlockingConnection(pika.URLParameters('amqps://zjdsjlug:RB7o2wtG3rRfPzuE4jhCk49jsSKnczmY@moose.rmq.cloudamqp.com/zjdsjlug?heartbeat=600'))

channel = connection.channel()
channel.queue_declare(queue='hello')


def publish(method, body):
    properties = pika.BasicProperties(method)
    print("Sending: [x]")
    channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(body), properties=properties)

    print(" [x] Sent 'Hello World!'")
    # connection.close()