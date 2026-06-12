"""Authentication, helpers, and shared runtime state."""

import time

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)

# Demo credentials. In production these would live in a secrets store / database.
VALID_API_KEYS = {"portfolio_showcase_key"}
ACCESS_TOKENS = {"demo_token": "api_developer"}


class AppState:
    """Tracks process lifetime and in-flight request count for the health check."""

    def __init__(self) -> None:
        self.start_time = time.monotonic()
        self.active_requests = 0

    @property
    def uptime_seconds(self) -> float:
        return round(time.monotonic() - self.start_time, 2)


state = AppState()


def validate_api_key(api_key: str = Security(api_key_header)) -> str:
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return api_key


def validate_token(token: str = Depends(oauth2_scheme)) -> str:
    if token not in ACCESS_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )
    return ACCESS_TOKENS[token]


def calculate_sentiment(text: str) -> float:
    """Mock sentiment analysis (replace with a real NLP model)."""
    positive_words = {"good", "great", "excellent", "amazing", "love", "enjoyable"}
    negative_words = {"bad", "terrible", "awful", "hate", "worst"}

    words = text.lower().split()
    total = len(words)
    if total == 0:
        return 0.0

    positive = sum(1 for word in words if word in positive_words)
    negative = sum(1 for word in words if word in negative_words)
    return round((positive - negative) / total * 10, 2)
