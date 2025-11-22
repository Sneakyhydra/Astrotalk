# 🌟 Astrological Insight Generator

A production-ready service that generates personalized daily astrological insights using zodiac logic and AI-powered language generation. Built with Python, Flask, and OpenAI.

## 📋 Features

- ✨ **AI-Powered Insights**: Generate personalized astrological predictions using OpenAI GPT
- 🔮 **Zodiac Calculation**: Automatic zodiac sign determination from birth date
- 🌍 **Multilingual Support**: English and Hindi output with native zodiac translations
- 🚀 **REST API**: Clean Flask API for easy integration
- 💻 **CLI Tool**: Interactive command-line interface
- 🗄️ **Smart Caching**: Daily insight caching to optimize API usage
- 📦 **Modular Architecture**: Extensible design for future enhancements
- 🔄 **Graceful Fallbacks**: Rule-based insights when LLM is unavailable

## 🚀 Quick Start

### Installation

1. **Clone and setup environment:**
   ```bash
   git clone <repository-url>
   cd Astrotalk
   make install
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   Get your API key from: https://platform.openai.com/api-keys

3. **Install OpenAI library (if not already installed):**
   ```bash
   ./venv/bin/pip install openai
   ```

### Running the Application

#### Option 1: REST API Server

```bash
python main.py
```

The API will be available at `http://localhost:5000`

#### Option 2: CLI Tool

```bash
python cli.py
```

Follow the interactive prompts to get your personalized insight.

## 📚 API Documentation

### Health Check

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "astrological-insight-generator"
}
```

### Get Zodiac Sign

Retrieve zodiac information from a birth date.

```bash
GET /api/zodiac?date=YYYY-MM-DD&language=en
```

**Parameters:**
- `date` (required): Birth date in YYYY-MM-DD format
- `language` (optional): Language code (`en` or `hi`). Default: `en`

**Example:**
```bash
curl "http://localhost:5000/api/zodiac?date=1995-08-20&language=en"
```

**Response:**
```json
{
  "sign": "Leo",
  "element": "Fire",
  "ruling_planet": "Sun",
  "traits": ["confident", "generous", "warm-hearted", "creative", "charismatic"],
  "date_range": "July 23 - August 22",
  "language": "en"
}
```

### Generate Insight

Generate a personalized astrological insight.

```bash
POST /api/insight
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Ritika",
  "birth_date": "1995-08-20",
  "birth_time": "14:30",
  "birth_place": "Jaipur, India",
  "language": "en"
}
```

**Fields:**
- `name` (required): User's name
- `birth_date` (required): Birth date in YYYY-MM-DD format
- `birth_time` (optional): Birth time in HH:MM format
- `birth_place` (optional): Birth location
- `language` (optional): Output language (`en` or `hi`). Default: `en`

**Example:**
```bash
curl -X POST http://localhost:5000/api/insight \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ritika",
    "birth_date": "1995-08-20",
    "birth_time": "14:30",
    "birth_place": "Jaipur, India",
    "language": "en"
  }'
```

**Response:**
```json
{
  "zodiac": "Leo",
  "insight": "Your innate leadership and warmth will shine today. Embrace spontaneity and avoid overthinking.",
  "language": "en",
  "element": "Fire",
  "ruling_planet": "Sun",
  "traits": ["confident", "generous", "warm-hearted", "creative", "charismatic"]
}
```

### Hindi Output Example

```bash
curl -X POST http://localhost:5000/api/insight \
  -H "Content-Type: application/json" \
  -d '{
    "name": "रितिका",
    "birth_date": "1995-08-20",
    "language": "hi"
  }'
```

**Response:**
```json
{
  "zodiac": "सिंह",
  "insight": "आपकी जन्मजात नेतृत्व क्षमता और गर्मजोशी आज चमकेगी...",
  "language": "hi"
}
```

## 🖥️ CLI Usage

Run the interactive CLI:

```bash
python cli.py
```

**Example Session:**
```
============================================================
🌟 Astrological Insight Generator 🌟
============================================================

Enter your name: Ritika
Enter your birth date (YYYY-MM-DD): 1995-08-20
Enter your birth place (optional): Jaipur, India
Choose language (en/hi) [default: en]: en
Output format (text/json) [default: text]: text

Generating your personalized insight...

============================================================
Name: Ritika
Zodiac Sign: Leo (Fire)
Ruling Planet: Sun
Key Traits: confident, generous, warm-hearted
============================================================

✨ Your Daily Insight ✨

Your innate leadership and warmth will shine today...

============================================================
```

**JSON Output:**
```bash
python cli.py
# Select 'json' as output format
```

## 🏗️ Architecture

### Project Structure

```
Astrotalk/
├── model/              # Data models and zodiac logic
│   ├── schemas.py      # BirthDetails, ZodiacInfo, InsightResponse
│   └── zodiac.py       # Zodiac calculation and traits
├── embedding/          # LLM integration
│   └── llm.py          # OpenAI wrapper for insight generation
├── languages/          # Translation utilities
│   └── translator.py   # Hindi translation and zodiac names
├── database/           # Data persistence
│   ├── qdrant.py       # Vector database client (future use)
│   └── cache.py        # In-memory insight caching
├── main.py             # Flask REST API
├── cli.py              # Command-line interface
└── .env                # Configuration
```

### Key Design Decisions

**1. Zodiac Calculation**
- Uses tropical zodiac (Western astrology)
- Date-based calculation from birth date
- Extensible for time/location-based calculations (ascendant, moon sign)

**2. LLM Integration**
- OpenAI GPT-3.5-turbo for insight generation
- Personalized prompts using zodiac traits and daily themes
- Graceful fallback to rule-based insights

**3. Caching Strategy**
- In-memory cache for daily insights per zodiac/language
- Reduces API costs and improves response time
- Extensible to Qdrant vector store for semantic retrieval

**4. Translation**
- OpenAI API for Hindi translation
- Maintains tone and astrological context
- Ready for IndicTrans2/NLLB integration

**5. Modularity**
- Clean separation of concerns
- Easy to plug in real Panchang APIs
- Ready for LangChain integration

## 🧪 Development

### Code Quality

The project uses strict code quality tools:

```bash
# Format code (isort + black)
make format

# Run linters (flake8 + mypy)
make lint

# Format and lint
make check
```

### Testing

```bash
# Run tests with coverage
make test
```

### Requirements

- Python 3.11 (strictly `>=3.11,<3.12`)
- 100 character line length
- Strict mypy type checking
- Black code style

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|----------|
| `OPENAI_API_KEY` | OpenAI API key for LLM | Yes (for AI features) | - |
| `PORT` | Server port | No | 5000 |
| `PYTHON_ENV` | Environment mode | No | production |
| `DEFAULT_LANGUAGE` | Default output language | No | en |
| `ENABLE_CACHING` | Enable insight caching | No | true |
| `LOG_LEVEL` | Logging verbosity | No | INFO |

### Optional: Qdrant Configuration

For future vector store integration:

- `QDRANT_HOST`
- `QDRANT_API_KEY`
- `QDRANT_*_COLLECTION_NAME`

## 🚀 Extension Points

### Future Enhancements

1. **Panchang Integration**
   - Replace simplified zodiac logic with real Vedic astrology calculations
   - Integrate APIs like DrikPanchang or AstroSage

2. **Vector Store**
   - Store astrological texts in Qdrant
   - Semantic retrieval for personalized insights
   - User profile embeddings for better personalization

3. **LangChain Integration**
   - Multi-step reasoning for complex predictions
   - Chain zodiac analysis → personality → daily guidance
   - Memory for conversation history

4. **Advanced Calculations**
   - Ascendant (rising sign) from birth time/location
   - Moon sign calculation
   - Planetary positions and transits

5. **More Languages**
   - Support for regional Indian languages
   - Integration with IndicTrans2 or NLLB

6. **User Profiles**
   - Store user preferences and history
   - Personalization based on past interactions
   - Subscription and notification system

## 📝 Example Use Cases

### 1. Daily Horoscope App
Integrate the API into a mobile/web app for daily horoscopes.

### 2. Chatbot Integration
Use as a backend for an astrological chatbot.

### 3. Content Generation
Generate astrological content for blogs or social media.

### 4. Personalization Engine
Use zodiac traits for user profiling and recommendations.

## 🤝 Contributing

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```

2. Install development dependencies:
   ```bash
   make install-dev
   ```

3. Make changes and ensure code quality:
   ```bash
   make check
   ```

4. Run tests:
   ```bash
   make test
   ```

5. Commit and push:
   ```bash
   git add .
   git commit -m "Add your feature"
   git push origin feature/your-feature
   ```

6. Open a pull request

## 📄 License

This project is for educational and demonstration purposes.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Qdrant for vector database
- Tropical zodiac system for astrological calculations
