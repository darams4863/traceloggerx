from fastapi import FastAPI, Request

from traceloggerx import set_logger

logger = set_logger("fastapi-example")

app = FastAPI()

@app.middleware("http")
async def add_logging(request: Request, call_next):
    trace_id = request.headers.get("X-Trace-ID", "anonymous")
    logger.info("Request started", extra={"trace_id": trace_id})
    response = await call_next(request)
    logger.info("Request ended", extra={"trace_id": trace_id})
    return response

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello, World!"}