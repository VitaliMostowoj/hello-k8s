from fastapi import FastAPI
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import os

app = FastAPI()

counter = int(os.getenv("COUNTER", 0))  # Get counter value from environment variable or default to 0

# Create a Prometheus Gauge metric to reflect the counter value
PROMETHEUS_COUNTER = Gauge("app_counter", "Counter value from FastAPI app")
PROMETHEUS_COUNTER.set(counter)  # Initialize with the current counter value

# Define a Prometheus Counter

@app.get("/")
async def root():
    node_name = os.getenv("MY_NODE_NAME", "unknown")
    pod_name = os.getenv("MY_POD_NAME", "unknown")
    pod_namespace = os.getenv("MY_POD_NAMESPACE", "unknown")
    pod_ip = os.getenv("MY_POD_IP", "unknown")

    return {"node_name": node_name, "pod_name": pod_name, "pod_namespace": pod_namespace, "pod_ip": pod_ip, "error_couter": counter}

#curl -X 'POST' 'http://127.0.0.1:8000/set_counter?value=10'

@app.post("/set_counter")
def set_counter(value: int):
    global counter
    counter = value
    os.environ["COUNTER"] = str(counter)  # Update environment variable
    PROMETHEUS_COUNTER.set(counter)  # Update Prometheus metric with new value
    return {"message": "Counter updated", "counter": counter}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)