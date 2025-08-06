run:
	uv run main.py

test:
	uv pip run pytest

logs:
	type logs/*.log || echo 'stdout logging only'

docker-build:
	docker build -t llmstart-bot .

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f