from decouple import config
from waitress import serve
import paho.mqtt.client as mqtt
import traceback
from argparse import ArgumentParser
from threading import Thread
from flask import Flask, Response
from .config import topics

topic_counter = {}
app = Flask(__name__)
for t in topics:
    topic_counter[t] = 0

@app.route('/mqtt_metrics')
def collect_metrics():
    metrics = ''
    try:
        for t in topics:
            metrics += create_metric('mqtt_msgcounter', t, topic_counter[t])
    except:
        print(traceback.format_exc())
    return Response(metrics, mimetype='text/plain')

def create_metric(name, topic, value):
    metric = ''
    metric += name
    metric += '{topic=\"'+topic+'\",} '+str(value)+'\n'
    return metric

def on_message(topic):
    topic_counter[topic] += 1


def connect_mqtt():
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--http-port', default=9630, help='HTTP Webserver port')
    args = parser.parse_args()

    mqtt_thread = Thread(target=connect_mqtt)
    mqtt_thread.start()

    thread = Thread(target=collect_metrics)
    thread.start()
    serve(app, host='0.0.0.0', port=args.http_port)