setup-dev:
    @echo "Setting up development environment..."
    @pip install -e '.[dev]'
    @echo "Done!"

format:
    @echo "Formating codes..."
    @ruff format ./
    @echo "Done!"

lint:
    @echo "Linting codes..."
    @ruff check ./
    @ruff format --check ./
    @echo "Done!"

test:
    @echo "Running tests..."
    @pytest --cov=requests_openapi
    @echo "Done!"
