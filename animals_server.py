# flask_server.py

from flask import Flask, request, jsonify
import uuid
import time
import random
import logging

# OpenTelemetry imports
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Set up resource
resource = Resource(attributes={
    SERVICE_NAME: "animal_server"
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
    name="requests_total",
    description="Total number of requests",
    unit="1",
)
error_counter = meter.create_counter(
    name="errors_total",
    description="Total number of errors",
    unit="1",
)
animal_counter = meter.create_counter(
    name="animal_added_total",
    description="Total number of animals added",
    unit="1",
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("animal_server")

# Instrument Flask and logging
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
LoggingInstrumentor().instrument(set_logging_format=True)

# Data storage
data_store = {}

# Validation rules
valid_animals = {
    "Horse": {"NumberOfLegs": 4, "Kind": "Mammal"},
    "Dog": {"NumberOfLegs": 4, "Kind": "Mammal"},
    "Cat": {"NumberOfLegs": 4, "Kind": "Mammal"},
    "Chicken": {"NumberOfLegs": 2, "Kind": "Bird"},
    "Chimpanzee": {"NumberOfLegs": 2, "Kind": "Mammal"},
    "Alligator": {"NumberOfLegs": 4, "Kind": "Reptile"},
}

valid_names = ["Fenris", "Oskar", "Rasmus", "Elvis"]

@app.route('/animals', methods=['PUT'])
def add_animal():
    with tracer.start_as_current_span("add_animal") as span:
        request_counter.add(1)
        animal = request.get_json()
        animal_name = animal.get("Name")
        animal_type = animal.get("Animal")
        if animal_name == "Elvis":
            # Simulate delay
            delay = random.uniform(2, 4)
            time.sleep(delay)
            span.set_attribute("delay", delay)

        # Validate animal
        valid = True
        reasons = []
        if animal_type not in valid_animals:
            valid = False
            reasons.append("Invalid animal type")
        else:
            expected = valid_animals[animal_type]
            if animal.get("NumberOfLegs") != expected["NumberOfLegs"]:
                valid = False
                reasons.append("Invalid number of legs for animal")
            if animal.get("Kind") != expected["Kind"]:
                valid = False
                reasons.append("Invalid kind for animal")

        if valid:
            # Special handling for Alligator
            if animal_type == "Alligator":
                if random.random() < 0.1:
                    error_counter.add(1)
                    logger.error("Alligator attacked the CPU and request failed")
                    return jsonify({"error": "Alligator caused an error"}), 500

            animal_id = str(uuid.uuid4())
            data_store[animal_id] = animal
            animal_counter.add(1)
            logger.info(f"Added {animal_type} with ID {animal_id}")
            return jsonify({"id": animal_id}), 201
        else:
            error_counter.add(1)
            logger.error(f"Failed to add {animal_type}: {', '.join(reasons)}")
            return jsonify({"error": reasons}), 400

@app.route('/animals/<animal_id>', methods=['GET'])
def get_animal(animal_id):
    with tracer.start_as_current_span("get_animal"):
        animal = data_store.get(animal_id)
        if animal:
            return jsonify(animal), 200
        else:
            return jsonify({"error": "Animal not found"}), 404

@app.route('/animals', methods=['GET'])
def list_animals():
    with tracer.start_as_current_span("list_animals"):
        return jsonify(list(data_store.keys())), 200

# Expose metrics endpoint
metrics_app = make_wsgi_app()
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': metrics_app
})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

