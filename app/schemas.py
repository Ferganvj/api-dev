"""Pydantic request/response models."""

import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class TextAnalysisRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=500,
        examples=["FastAPI makes building APIs enjoyable!"],
    )
    analysis_type: Literal["basic", "advanced"] = Field(
        "basic",
        examples=["advanced"],
        description="Analysis depth: 'basic' or 'advanced'",
    )


class AnalysisResult(BaseModel):
    request_id: str
    timestamp: datetime.datetime
    word_count: int
    character_count: int
    unique_words: int
    avg_word_length: float
    sentiment_score: Optional[float] = Field(
        None,
        description="Only available in advanced analysis",
    )
    processing_time_ms: float


class SystemHealth(BaseModel):
    status: str
    version: str
    uptime_seconds: float
    active_requests: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
