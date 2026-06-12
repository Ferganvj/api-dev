# How to use API

1. Run the API:

```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

   Run the tests:

```
pytest
```

2. Access Interactive Documentation:
    - Open `http://localhost:8000/docs` in your browser
    - Try endpoints with exampl payloads

3. Demonstrate Features:

```

# Get access token
curl -X POST http://localhost:8000/token

# Analyze text (with authentication)
curl -X POST http://localhost:8000/analyze-text \
  -H "Authorization: Bearer demo_token" \
  -H "Content-Type: application/json" \
  -d '{"text": "FastAPI makes building APIs enjoyable!", "analysis_type": "advanced"}'

# Health check (with API key)
curl -X GET http://localhost:8000/system/health \
  -H "X-API-KEY: portfolio_showcase_key"
```

## Key features

API Design

- RESTful endpoints with proper HTTP methods

- Semantic versioning (v2.1.0)

- Comprehensive OpenAPI documentation

- Tag-based endpoint organization

Security Implementation

- API key authentication

- OAuth2 password flow simulation

- Header-based security

- Dependency injection for authorization

Data Validation

- Pydantic models for request/response

- Field validation with constraints

- Automatic documentation generation

- Example payloads in schemas

Production-Ready Features

- Unique request IDs

- Processing time metrics

- Health monitoring endpoint

- Error handling with request IDs

- Versioned API

Scalable Architecture

- Modular design patterns

- Separation of concerns

- Mock sentiment analysis (replace with real model)

- Async-ready endpoints

## Key takeaways:

- **Security Implementation**  
  API key authentication + OAuth2 simulation showing understanding of authorization flows

- **Production-Grade Features**  
  Request IDs, performance metrics, and health checks demonstrate operational awareness

- **Professional Documentation**  
  Auto-generated OpenAPI docs with examples show commitment to usability

- **Clean Architecture**  
  Separation of concerns with routes, models, and services highlights maintainable design