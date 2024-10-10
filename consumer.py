import pika, json
from main import Product, db, app

connection = pika.BlockingConnection(
    pika.URLParameters('amqps://zjdsjlug:RB7o2wtG3rRfPzuE4jhCk49jsSKnczmY@moose.rmq.cloudamqp.com/zjdsjlug?heartbeat=600'))
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='flask_ms-rabbitmq-1'))

channel = connection.channel()
channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    with app.app_context():
        data = json.loads(body)
        print(f" [x] Received {body}")
        print(f" [y] Properties {properties}")
        print(data)

        if properties.content_type == "product_created":
            product = Product(id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
            db.session.commit()
            print("data")
            print("data")


        elif properties.content_type == 'product_updated':
            product = Product.query.get_or_404(data['id'])
            product.title = data['title']
            product.image = data['image']
            db.session.commit()


        elif properties.content_type == 'product_deleted':
            product = Product.query.get_or_404(data['id'])
            db.session.delete(product)
            db.session.commit()


channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print("---")
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

# channel.close()