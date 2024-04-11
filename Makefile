compose_up:
	docker-compose up -d --wait && alembic upgrade head
compose_down:
	docker-compose down
test:
	export PYTHONPATH=. && pytest tests