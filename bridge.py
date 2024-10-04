import json 
from flask import Flask, request
import pika
import os

app = Flask(__name__)

# RabbitMQ connection details
rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
rabbitmq_port = int(os.environ.get('RABBITMQ_PORT', 15672))
rabbitmq_user = os.environ.get('RABBITMQ_USER', 'guest')
rabbitmq_pass = os.environ.get('RABBITMQ_PASS', 'guest')
rabbitmq_queue = os.environ.get('RABBITMQ_QUEUE', 'minio_events')

@app.route('/events', methods=['POST'])
def receive_event():
    event = request.json
       
       # Connect to RabbitMQ
    connection = pika.BlockingConnection(
           pika.ConnectionParameters(
               host=rabbitmq_host,
               port=rabbitmq_port,
               credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
           )
       )
    channel = connection.channel()
       
       # Declare the queue
    channel.queue_declare(queue=rabbitmq_queue, durable=True)
       
       # Send the event to RabbitMQ
    channel.basic_publish(
           exchange='',
           routing_key=rabbitmq_queue,
           body=json.dumps(event),
           properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
       )
       
    connection.close()

    return "Event received and sent to RabbitMQ", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)