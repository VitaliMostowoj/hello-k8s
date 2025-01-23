from fastapi import FastAPI
import os
app = FastAPI()


@app.get("/")
async def root():
    pod_name = os.getenv("MY_POD_NAME", "unknown")
    node_name = os.getenv("MY_NODE_NAME", "unknown")
    return {"pod_name": pod_name, "node_name": node_name}

