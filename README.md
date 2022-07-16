# mqtt-observer
A python based mqtt-metric-provider for prometheus-export 

## install 
```sh
git clone https://github.com/GiancarloRizzo/mqtt-observer.git

source bin/activate
```

## customize configuration in config.py
```python
# mqtt-defaults
broker = localhost
port   = 1883
qos    = 2

topics = [
    'topic_1',
    'topic_2',
     #
]

# scrape-defaults for prometheus
scrape_destination = 'localhost' 
scrape_port = 9630
scrape_url = '/mqtt_metrics'
```

## start
```sh
python3 mqtt-observer.py
```

## check via console if metrics are provided
```sh
curl localhost:9630/mqtt_metrics
```

## add target to your prometheus-scrape-config
```sh
# in /etc/prometheus/prometheus.yml you have to add:
# scrape_configs:
# previous scrape_targets
# ...
  - job_name: mqtt_metrics
    metrics_path: /mqtt_metrics
    static_configs:
    - targets:
      - localhost:9639
```