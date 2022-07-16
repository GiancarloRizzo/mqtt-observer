from decouple import config
from waitress import serve
import paho.mqtt.client as mqtt
import traceback
from argparse import ArgumentParser
from threading import Thread
from flask import Flask, Response
from config import topics

topic_counter = {}
topic_bytes   = {}

app = Flask(__name__)

def load_topics():
    for t in topics:
        topic_counter[t] = 0
        topic_bytes[t] = 0

@app.route('/mqtt_metrics')
def collect_metrics():
    metrics = ''
    try:
        for t in topics:
            metrics += create_metric('mqtt_msgcounter', t, topic_counter[t])
            metrics += create_metric('mqtt_bytes_in', t, topic_bytes[t])
    except:
        print(traceback.format_exc())
    return Response(metrics, mimetype='text/plain')

def create_metric(name, topic, value):
    metric = ''
    metric += name
    metric += '{topic=\"'+topic+'\",} '+str(value)+'\n'
    return metric



def on_message(client, userdata, message):
    if message.topic in topic_counter:
        topic_counter[message.topic] += 1
        topic_bytes[message.topic] += len(str(message.payload).encode('utf-8'))/8


def connect_mqtt():
    client = mqtt.Client()
    #for t in topics:
        #client.message_callback_add(t, on_message)
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.subscribe('#')
    client.loop_forever()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--http-port', default=9630, help='HTTP Webserver port')
    args = parser.parse_args()