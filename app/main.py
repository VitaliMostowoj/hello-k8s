from fastapi import FastAPI
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import os

app = FastAPI()

livez = True
readyz = True

gauge = int(os.getenv("COUNTER", 1))

PROMETHEUS_GAUGE = Gauge("app_counter", "Counter value from FastAPI app")
PROMETHEUS_GAUGE.set(gauge)  # Initialize with the current counter value


# curl -X 'POST' 'http://127.0.0.1:8000/set_counter?value=10'
@app.post("/set_gauge")
async def set_counter(value: int):
    global gauge
    gauge = value
    os.environ["COUNTER"] = str(gauge)  # Update environment variable
    PROMETHEUS_GAUGE.set(gauge)  # Update Prometheus metric with new value
    return {"message": "Counter updated", "counter": gauge}


@app.post("/set_livez")
async def set_livez(status: bool):
    global livez
    livez = status
    return {"livez was set to": status}


@app.post("/set_readyz")
async def set_readyz(status: bool):
    global readyz
    readyz = status
    return {"readyz was set to": status}


@app.get("/")
async def root():
    node_name = os.getenv("MY_NODE_NAME", "unknown")
    pod_name = os.getenv("MY_POD_NAME", "unknown")
    pod_namespace = os.getenv("MY_POD_NAMESPACE", "unknown")
    pod_ip = os.getenv("MY_POD_IP", "unknown")

    return {"node_name": node_name, "pod_name": pod_name, "pod_namespace": pod_namespace, "pod_ip": pod_ip,
            "error_gauge": gauge}


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/livez")
async def livez():
    if livez:
        return Response(content="ok", media_type="text/plain", status_code=200)
    else:
        return Response(content="not ok", media_type="text/plain", status_code=500)


@app.get("/readyz")
async def readyz():
    if readyz:
        return Response(content="ok", media_type="text/plain", status_code=200)
    else:
        return Response(content="not ok", media_type="text/plain", status_code=500)
