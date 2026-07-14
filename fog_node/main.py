from fastapi import FastAPI

from fog_node.api.routes import router
app = FastAPI(
    title="Digital Twin Fog Node",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Digital Twin Fog Node is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }