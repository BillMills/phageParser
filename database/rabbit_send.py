import pika, logging, datetime

a = str(datetime.date.today())
logging.basicConfig(filename='Rabbit_Send_'+a+'.log',level=logging.WARNING, format='%(asctime)s %(message)s')

def send(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.56.8'))
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_orientdb',
                             type='topic',
                             durable=True)

    routing_key = 'orientdb'
    channel.basic_publish(exchange='topic_orientdb',
                          routing_key=routing_key,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    logging.debug(" [x] Sent %r:%r" % (routing_key, message))
    connection.close()