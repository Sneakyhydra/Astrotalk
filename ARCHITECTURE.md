# Architecture & Design Decisions

This document provides detailed insights into the technical decisions made during the development of the Astrological Insight Generator.

## Table of Contents

1. [System Overview](#system-overview)
2. [Technology Choices](#technology-choices)
3. [Architecture Patterns](#architecture-patterns)
4. [Data Flow](#data-flow)
5. [Extension Points](#extension-points)
6. [Trade-offs & Assumptions](#trade-offs--assumptions)

## System Overview

The Astrological Insight Generator is a modular service that combines traditional astrological knowledge with modern AI/ML capabilities to generate personalized daily insights.

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                    (CLI / REST API Client)                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      Flask REST API                          │
│                     (main.py)                                │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  /health    /api/zodiac    /api/insight              │  │
│  └───────────────────────────────────────────────────────┘  │
└──────┬──────────────────────────────┬───────────────────────┘
       │                               │
       ▼                               ▼
┌─────────────────┐           ┌────────────────────┐
│  Zodiac Logic   │           │   LLM Integration  │
│  (model/)       │           │   (embedding/)     │
│                 │           │                    │
│ • calculate_    │           │ • OpenAI GPT-3.5   │
│   zodiac_sign() │           │ • Prompt           │
│ • get_zodiac_   │           │   engineering      │
│   info()        │           │ • Fallback logic   │
└─────────────────┘           └──────────┬─────────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │    Translation       │
                              │    (languages/)      │
                              │                      │
                              │  • Hindi support     │
                              │  • Zodiac names      │
                              └──────────────────────┘
       ┌──────────────────────────────┐
       │      Caching Layer           │
       │      (database/cache.py)     │
       │                              │
       │  • Daily insights cache      │
       │  • Per zodiac + language     │
       └──────────────────────────────┘
```

## Technology Choices

### 1. Python 3.11

**Why Python?**
- Rich ecosystem for AI/ML (OpenAI, transformers, NLTK)
- Excellent for rapid prototyping
- Strong typing support with mypy
- Production-ready with proper tooling

**Why 3.11 specifically?**
- Modern type hints (PEP 604: Union types with `|`)
- Performance improvements over 3.10
- Better error messages
- Active LTS support

### 2. Flask

**Alternatives Considered:** FastAPI, Django

**Why Flask?**
- Lightweight and minimal overhead
- Easy to understand and extend
- Sufficient for current requirements
- Already in project dependencies

**Trade-off:** No async support by default
- **Mitigation:** Current workload is I/O-bound (LLM calls) but sequential per request
- **Future:** Can migrate to FastAPI if async becomes critical

### 3. OpenAI GPT-3.5-turbo

**Alternatives Considered:** 
- Open-source models (LLaMA, Mistral)
- HuggingFace transformers
- Claude, Gemini

**Why OpenAI?**
- Excellent output quality for natural language
- Good Hindi support
- Reliable API with good uptime
- Reasonable pricing for prototype/MVP
- Simple integration

**Trade-offs:**
- Cost per request (mitigated by caching)
- External dependency (mitigated by fallback logic)
- Data sent to third party (acceptable for non-sensitive astrological data)

### 4. In-Memory Caching

**Why not Redis/Memcached?**
- Simplifies deployment (no external dependencies)
- Sufficient for single-instance deployment
- Daily insights don't need persistence across restarts
- Easy to migrate to Redis later

**When to upgrade:**
- Multi-instance deployment
- Need for cache persistence
- Cache warming strategies

## Architecture Patterns

### 1. Singleton Pattern (Database Clients)

```python
_qdrant_client = None

def get_qdrant_client() -> QdrantClient:
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(...)
    return _qdrant_client
```

**Rationale:**
- Expensive to create new connections
- Single client can handle multiple requests
- Prevents connection pool exhaustion

### 2. Dependency Injection (Loose Coupling)

Each module exposes clean interfaces:
- `calculate_zodiac_sign(date) -> str`
- `generate_insight(name, zodiac_info, language) -> str`
- `translate_text(text, language) -> str`

**Benefits:**
- Easy to test (can mock individual functions)
- Easy to swap implementations
- Clear contracts between components

### 3. Graceful Degradation

```python
if use_llm and os.getenv("OPENAI_API_KEY"):
    try:
        insight = _generate_insight_with_llm(...)
    except Exception:
        insight = _generate_fallback_insight(...)
else:
    insight = _generate_fallback_insight(...)
```

**Rationale:**
- Service remains functional without API key
- Demo/testing without costs
- Resilient to API failures

### 4. Dataclass Models

Using Python dataclasses for type safety and validation:

```python
@dataclass
class BirthDetails:
    name: str
    birth_date: date
    
    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Name cannot be empty")
```

**Benefits:**
- Automatic `__init__`, `__repr__`, `__eq__`
- Type hints enforced by mypy
- Validation at construction time
- Serialization support

## Data Flow

### Insight Generation Flow

```
1. User Request
   └─→ POST /api/insight
       {name, birth_date, language}

2. Validation & Parsing
   └─→ BirthDetails dataclass creation
   └─→ Date validation

3. Zodiac Calculation
   └─→ calculate_zodiac_sign(birth_date)
   └─→ get_zodiac_info(zodiac_sign)

4. Cache Check
   └─→ cache.get(zodiac_sign, language)
   └─→ If HIT: return cached insight
   └─→ If MISS: continue

5. Insight Generation
   └─→ generate_insight(name, zodiac_info, language)
       ├─→ If use_llm: OpenAI API call
       │   ├─→ Construct personalized prompt
       │   ├─→ Include zodiac traits + daily theme
       │   └─→ Generate with GPT-3.5-turbo
       └─→ Else: rule-based selection

6. Translation (if needed)
   └─→ If language == 'hi' and LLM available:
       └─→ translate_text(insight, 'hi')

7. Cache Store
   └─→ cache.set(zodiac_sign, language, insight)

8. Response
   └─→ InsightResponse dataclass
   └─→ JSON serialization
   └─→ Return to client
```

### Zodiac Calculation Logic

**Tropical Zodiac System:**
- Based on seasons (equinoxes and solstices)
- Most common in Western astrology
- Date ranges fixed relative to calendar

**Implementation:**
```python
# Check if date falls within zodiac date range
for sign, start, end in ZODIAC_DATES:
    if date_in_range(birth_date, start, end):
        return sign
```

**Special Case:** Capricorn spans year boundary (Dec 22 - Jan 19)

## Extension Points

### 1. Panchang Integration

**Current:** Simplified tropical zodiac calculation

**Future:** 
```python
from panchang_api import calculate_vedic_chart

def get_vedic_predictions(birth_details):
    chart = calculate_vedic_chart(
        date=birth_details.birth_date,
        time=birth_details.birth_time,
        location=birth_details.birth_place
    )
    return chart.predictions
```

**APIs to consider:**
- DrikPanchang API
- AstroSage API
- Swiss Ephemeris (local calculation)

### 2. Vector Store for Semantic Retrieval

**Current:** Fixed traits per zodiac

**Future:**
```python
# Store astrological texts in Qdrant
qdrant.add(
    collection="astrology_texts",
    documents=[
        "Leo individuals are natural leaders...",
        "During Mercury retrograde, Leo may experience..."
    ]
)

# Retrieve relevant context for insight generation
context = qdrant.query(
    collection="astrology_texts",
    query=f"{zodiac_sign} {theme} prediction"
)

# Use context in LLM prompt
prompt = f"Based on: {context}\nGenerate insight for {name}..."
```

### 3. LangChain Integration

**Current:** Single-shot LLM generation

**Future:**
```python
from langchain import LLMChain, PromptTemplate

# Multi-step reasoning
chain = (
    analyze_zodiac_traits 
    | identify_daily_influences 
    | generate_personalized_insight
)

insight = chain.run(birth_details=details)
```

### 4. User Profiles & Personalization

**Current:** Name-based personalization only

**Future:**
```python
class UserProfile:
    preferences: dict
    history: list[InsightResponse]
    feedback: list[Rating]
    
def generate_personalized_insight(user_profile):
    # Analyze past insights user liked
    # Adjust tone/style based on preferences
    # Consider zodiac compatibility with recent events
```

## Trade-offs & Assumptions

### Assumptions

1. **Single Language per Request**
   - User specifies desired language upfront
   - No auto-detection needed
   - **Future:** Could add language detection for text input

2. **Tropical Zodiac System**
   - Assumes Western astrology preference
   - **Alternative:** Support Vedic (sidereal) zodiac as option

3. **Daily Insights are Zodiac-Level**
   - Same insight for all users of same zodiac + language on same day
   - **Future:** User-specific insights based on birth chart

4. **No Authentication**
   - Open API for demo/MVP
   - **Future:** Add API keys, rate limiting, user accounts

5. **Birth Time/Location Optional**
   - Currently not used for calculations
   - **Future:** Required for ascendant/moon sign calculations

### Trade-offs

| Decision | Benefit | Cost | Mitigation |
|----------|---------|------|------------|
| OpenAI API | Quality insights | API costs | Caching, fallbacks |
| In-memory cache | Simplicity | No persistence | Acceptable for daily data |
| Simplified zodiac | Fast, no external deps | Less accurate | Document as limitation |
| Synchronous Flask | Simple code | Slower for concurrent requests | Sufficient for MVP |
| No auth | Easy to demo | Security risk | Add for production |

### Performance Considerations

**Current Bottlenecks:**
1. OpenAI API latency (~1-3s per request)
2. Translation as separate API call (+1-2s for Hindi)

**Optimizations:**
1. ✅ Caching eliminates repeat API calls
2. 🔄 Could parallelize insight + translation
3. 🔄 Could use batch APIs for multiple users
4. 🔄 Could pre-generate insights for all zodiacs daily

**Scalability:**
- **Current:** Can handle ~100 req/min (limited by API rate limits)
- **With caching:** Can handle ~1000 req/min (12 zodiac signs × 2 languages = 24 unique daily insights)
- **With optimization:** ~10,000 req/min (horizontal scaling + CDN caching)

## Code Quality Standards

### Type Safety

**Strict mypy configuration:**
```toml
[tool.mypy]
strict = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
```

**Every function has type annotations:**
```python
def calculate_zodiac_sign(birth_date: date) -> str:
    ...
```

### Error Handling

**Structured error responses:**
```python
return jsonify({"error": "Invalid date format"}), 400
```

**Graceful degradation:**
```python
try:
    insight = llm_generate()
except Exception:
    insight = fallback_generate()
```

### Testing Strategy

**Current state:** Foundation for testing in place

**Recommended tests:**
1. Unit tests for zodiac calculation
2. Unit tests for date range edge cases (year boundaries)
3. Mock tests for LLM integration
4. API endpoint integration tests
5. CLI flow tests

**Example:**
```python
def test_zodiac_calculation():
    assert calculate_zodiac_sign(date(1995, 8, 20)) == "Leo"
    assert calculate_zodiac_sign(date(1995, 12, 22)) == "Capricorn"
```

## Security Considerations

### Current Implementation

1. **API Key Management**
   - ✅ Stored in environment variables
   - ✅ Not in code or version control
   - ✅ Documented in .env.example

2. **Input Validation**
   - ✅ Date format validation
   - ✅ Name presence check
   - ✅ Language whitelist
   - 🔄 Could add: length limits, sanitization

3. **Error Messages**
   - ✅ Don't expose internal details
   - ✅ Generic error messages
   - 🔄 Could add: error tracking/logging

### Production Hardening Checklist

- [ ] Rate limiting (per IP/API key)
- [ ] Request size limits
- [ ] CORS configuration
- [ ] HTTPS enforcement
- [ ] API key authentication
- [ ] Logging and monitoring
- [ ] DDoS protection
- [ ] Input sanitization for all fields
- [ ] Secrets rotation policy

## Deployment Considerations

### Current Setup
- Single-instance Flask server
- In-memory cache
- Environment-based configuration

### Production Deployment Options

**1. Container (Docker)**
```dockerfile
FROM python:3.11-slim
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

**2. Cloud Platforms**
- Heroku (simple, auto-scaling)
- AWS ECS/Lambda (serverless)
- Google Cloud Run (containers)
- Railway, Render (quick deploy)

**3. Scaling Strategy**
- Load balancer → Multiple Flask instances
- Shared Redis cache
- CDN for static content
- Queue for async processing

## Future Roadmap

### Phase 1: MVP (Current)
- ✅ Zodiac calculation
- ✅ AI-generated insights
- ✅ Hindi translation
- ✅ REST API + CLI
- ✅ Caching

### Phase 2: Enhanced Personalization
- User accounts and profiles
- Birth chart calculations (ascendant, moon sign)
- Historical insight tracking
- Feedback collection

### Phase 3: Advanced Features
- Panchang integration
- Planetary transits
- Compatibility analysis
- Vector store for astrological texts

### Phase 4: Scale & Monetization
- Mobile apps (iOS/Android)
- Subscription tiers
- Premium insights
- Push notifications
- Multi-language support (regional Indian languages)

---

**Document Version:** 1.0  
**Last Updated:** 2025-11-22  
**Author:** Technical Team
