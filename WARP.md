# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Astrotalk is a Python library for astrology predictions that uses Qdrant vector database for storing and querying astrology-related embeddings. The project leverages sentence transformers for embeddings and NLTK for natural language processing.

## Development Commands

### Environment Setup
```bash
# Create virtual environment and install production dependencies
make install

# Create virtual environment and install development dependencies
make install-dev
```

### Code Quality
```bash
# Format code (isort + black)
make format

# Run linters (flake8 + mypy)
make lint

# Format and lint in one step
make check
```

### Testing
```bash
# Run all tests with coverage
make test

# Set PYTHON_ENV=test when running tests manually
PYTHON_ENV=test ./venv/bin/pytest --cov=. --cov-report=term-missing
```

### Running the Application
```bash
# Run the main application
python main.py
```

### Cleanup
```bash
# Clean build artifacts, caches, and coverage reports
make clean
```

## Architecture

### Module Structure

- **`database/`**: Qdrant vector database client management
  - `qdrant.py`: Singleton pattern for Qdrant client initialization using environment variables
  
- **`embedding/`**: Embedding generation utilities (currently empty but intended for sentence transformers integration)

- **`languages/`**: Language processing utilities (placeholder for NLTK-based features)

- **`model/`**: Data models and schemas (placeholder for astrology domain models)

- **`main.py`**: Application entry point

### Key Architectural Patterns

**Singleton Database Client**: The Qdrant client is initialized once and reused throughout the application via `get_qdrant_client()` in `database/qdrant.py`. It requires `QDRANT_HOST` and `QDRANT_API_KEY` environment variables.

**Vector Collections**: The project uses four Qdrant collections for different astrology domains:
- `zodiac`: Zodiac sign information
- `astrology`: General astrology data
- `personality`: Personality trait embeddings
- `relationship`: Relationship compatibility data

Collection names are configured via environment variables (e.g., `QDRANT_ZODIAC_COLLECTION_NAME`).

## Python Version and Dependencies

- **Python Version**: 3.11 (strictly `>=3.11,<3.12`)
- **Key Dependencies**: 
  - `qdrant-client`: Vector database client
  - `sentence-transformers`: Text embedding generation
  - `nltk`: Natural language processing
  - `python-dotenv`: Environment variable management
  - `flask`: Web framework

## Code Style Configuration

- **Line Length**: 100 characters (enforced by black, flake8, and isort)
- **Import Sorting**: black profile for isort
- **Type Checking**: Strict mypy configuration with full type hints required
- **Flake8**: Ignores E203 (whitespace before ':') and W503 (line break before binary operator)

## Environment Variables

Required variables (see `.env.example`):
- `QDRANT_HOST`: Qdrant server URL
- `QDRANT_API_KEY`: Authentication key
- `QDRANT_ZODIAC_COLLECTION_NAME`: Collection name for zodiac data
- `QDRANT_ASTROLOGY_COLLECTION_NAME`: Collection name for astrology data
- `QDRANT_PERSONALITY_COLLECTION_NAME`: Collection name for personality data
- `QDRANT_RELATIONSHIP_COLLECTION_NAME`: Collection name for relationship data
- `PYTHON_ENV`: Environment mode (development/test)
- `LOG_LEVEL`: Logging verbosity

## Development Workflow

When making changes:
1. Always run `make check` before committing (formats and lints code)
2. Run `make test` to ensure tests pass
3. The project uses strict mypy - all functions must have type annotations
4. Follow the black code style (100 character line length)
5. Import sorting is automatic with isort using black profile
