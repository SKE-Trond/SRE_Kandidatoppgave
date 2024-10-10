# nagging_client.py

import requests
import random
import time
import threading
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from prometheus_client import make_wsgi_app
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Set up resource
resource = Resource(attributes={
    SERVICE_NAME: "animal_client"
})

# Set up tracing
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)
otlp_exporter = OTLPSpanExporter()
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Set up metrics
reader = PrometheusMetricReader()
metrics.set_meter_provider(MeterProvider(metric_readers=[reader], resource=resource))
meter = metrics.get_meter(__name__)

# Create metrics
request_counter = meter.create_counter(
    name="requests_sent_total",
    description="Total number of requests sent",
    unit="1",
)
error_counter = meter.create_counter(
    name="errors_total",
    description="Total number of errors",
    unit="1",
)

# Valid values
animals = ["Horse", "Dog", "Cat", "Chicken", "Chimpanzee", "Alligator"]
number_of_legs_options = [2, 4, 0]
kinds = ["Mammal", "Reptile", "Bird"]
names = ["Fenris", "Oscar", "Rasmus", "Elvis"]

# Server address
SERVER_URL = "http://animal_server:5000/animals"  # Replace 'server' with actual server address

def send_random_requests():
    while True:
        with tracer.start_as_current_span("send_request") as span:
            animal = {
                "Animal": random.choice(animals),
                "NumberOfLegs": random.choice(number_of_legs_options),
                "Kind": random.choice(kinds),
                "Name": random.choice(names),
            }
            try:
                response = requests.put(SERVER_URL, json=animal)
                request_counter.add(1)
                if response.status_code == 201:
                    span.set_attribute("request.success", True)
                else:
                    error_counter.add(1)
                    span.set_attribute("request.success", False)
            except Exception as e:
                error_counter.add(1)
                span.set_attribute("request.success", False)
        time.sleep(random.uniform(0.1, 1))

# Expose metrics endpoint
app = Flask(__name__)
metrics_app = make_wsgi_app()
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': metrics_app
})

if __name__ == '__main__':
    threading.Thread(target=send_random_requests).start()
    app.run(host='0.0.0.0', port=8000)

