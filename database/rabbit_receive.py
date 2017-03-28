import pika, orient, logging, datetime

a = str(datetime.date.today())
logging.basicConfig(filename='Rabbit_Receive_'+a+'.log',level=logging.WARNING, format='%(asctime)s %(message)s')

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.56.8'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_orientdb',
                         type='topic',
                         durable=True)

queue_name = 'Orientdb'
result = channel.queue_declare(queue=queue_name, durable=True)

binding_keys = ['orientdb']

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_orientdb',
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    logging.debug(" [x] %r:%r" % (method.routing_key, body))
    orient.orient_command(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

try:
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,
                        queue=queue_name)
    channel.start_consuming()
except Exception as e:
    logging.error(e)