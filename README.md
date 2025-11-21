# Astrotalk

## Setup

1. Create/activate a virtual environment:
   ```bash
   make setup
   ```
2. Install dependencies:
   ```bash
   make install
   ```
3. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
4. Configure environment variables in the `.env` file as needed.
5. Run the application:
   ```bash
   python main.py
   ```

## Contributing

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
2. Create/activate a virtual environment:
   ```bash
   make setup
   ```
3. Install development dependencies:
   ```bash
   make install-dev
   ```
4. Create a `.env` file from the example if you haven't already:
   ```bash
   cp .env.example .env
   ```
5. Make your changes and ensure code quality:
   ```bash
   make check
   ```
6. Run tests to ensure everything works:
   ```bash
   make test
   ```
7. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Add your commit message"
   git push origin feature/your-feature
   ```
8. Open a pull request for review.
