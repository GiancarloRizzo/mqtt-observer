# mqtt-defaults
broker = localhost
port   = 1883
qos    = 2
topics = [
    "topic/1",
    "topic/2",
]


# scrape-defaults for prometheus
scrape_destination = 'localhost' 
scrape_port = 9630
scrape_url = '/mqtt_metrics'