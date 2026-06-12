"""Core API: app construction, middleware, error handling, and routes."""

import datetime
import uuid

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from . import __version__
from .dependencies import (
    calculate_sentiment,
    state,
    validate_api_key,
    validate_token,
)
from .schemas import AnalysisResult, SystemHealth, TextAnalysisRequest, TokenResponse

app = FastAPI(
    title="Showcase API",
    description="API development showcase: auth, validation, and observability.",
    version=__version__,
    openapi_tags=[
        {"name": "Authentication", "description": "Secure API key and token endpoints"},
        {"name": "Data Processing", "description": "Core business logic endpoints"},
        {"name": "System", "description": "Health checks and diagnostics"},
    ],
)


@app.middleware("http")
async def track_active_requests(request: Request, call_next):
    """Maintain a live in-flight request count for the health endpoint."""
    state.active_requests += 1
    try:
        return await call_next(request)
    finally:
        state.active_requests -= 1


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "request_id": request.headers.get("X-Request-ID", str(uuid.uuid4())),
        },
    )


@app.post("/token", response_model=TokenResponse, tags=["Authentication"])
async def generate_token():
    """OAuth2 token endpoint (simulated)."""
    return TokenResponse(access_token="demo_token", token_type="bearer")


@app.post(
    "/analyze-text",
    response_model=AnalysisResult,
    tags=["Data Processing"],
    summary="Text analysis endpoint",
    description="Data processing with configurable options.",
)
async def analyze_text(
    request: TextAnalysisRequest,
    user: str = Depends(validate_token),
):
    """Text analysis with metrics and optional sentiment scoring."""
    start_time = datetime.datetime.now(datetime.timezone.utc)

    words = request.text.split()
    word_count = len(words)
    char_count = len(request.text)
    unique_words = len(set(words))
    avg_length = sum(len(word) for word in words) / word_count if word_count else 0.0

    sentiment = None
    if request.analysis_type == "advanced":
        sentiment = calculate_sentiment(request.text)

    now = datetime.datetime.now(datetime.timezone.utc)
    return AnalysisResult(
        request_id=str(uuid.uuid4()),
        timestamp=now,
        word_count=word_count,
        character_count=char_count,
        unique_words=unique_words,
        avg_word_length=round(avg_length, 2),
        sentiment_score=sentiment,
        processing_time_ms=round((now - start_time).total_seconds() * 1000, 2),
    )


@app.get(
    "/system/health",
    response_model=SystemHealth,
    tags=["System"],
    summary="System health check",
)
async def health_check(api_key: str = Depends(validate_api_key)):
    """Operational health and live diagnostics."""
    return SystemHealth(
        status="operational",
        version=app.version,
        uptime_seconds=state.uptime_seconds,
        active_requests=state.active_requests,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
