import time
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from slowapi import Limiter, _rate_limit_exceeded_handler
import prometheus_fastapi_instrumentator
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.routes import auth
from app.core.config import settings
from app.core.events import event_publisher
from app.services.metrics_service import metrics_service

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Set up rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)

# Configurar Prometheus para Grafana Cloud
instrumentator = prometheus_fastapi_instrumentator.Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[".*admin.*", "/metrics"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="inprogress",
    inprogress_labels=True,
)

@app.on_event("startup")
async def startup_prometheus():
    instrumentator.instrument(app).expose(app, include_in_schema=False, should_gzip=True)


# Set up logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    duration_ms = process_time * 1000
    
    # Log request
    logger.info(
        f"Request: {request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Time: {process_time:.4f}s"
    )
    
    # Record metrics in Grafana
    metrics_service.record_request(
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=duration_ms
    )
    
    return response


@app.on_event("startup")
async def startup_event():
    # Initialize Grafana metrics
    metrics_service.initialize()
    logger.info("Auth Login/Signup Service started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    # Disconnect from message broker
    await event_publisher.disconnect()
    logger.info("Auth Login/Signup Service shutdown successfully")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
