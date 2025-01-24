from fastapi import FastAPI
import os

app = FastAPI()


@app.get("/")
async def root():
    node_name = os.getenv("MY_NODE_NAME", "unknown")
    pod_name = os.getenv("MY_POD_NAME", "unknown")
    pod_namespace = os.getenv("MY_POD_NAMESPACE", "unknown")
    pod_ip = os.getenv("MY_POD_IP", "unknown")

    return {"node_name": node_name, "pod_name": pod_name, "pod_namespace": pod_namespace, "pod_ip": pod_ip}
