ENV_FILE=.env
include $(ENV_FILE)
export


PYTEST_TARGET ?= tests
PYTEST_ARGS ?= -vv -x






run:
	PYTHONPATH=src:. flask --app 'wallet:create_app()' run --host=0.0.0.0 --debug
	
test:
	docker exec -it wallet coverage run -m pytest $(PYTEST_ARGS) $(PYTEST_TARGET) && coverage report

cs:
	autoflake . && black . && isort .

migrate:
	docker exec -it wallet pw_migrate migrate --database 'postgresql://$(DB_USER):$(DB_PASS)@pgdb:5432/$(DB_NAME)' --directory wallet/migrations

up:
	docker compose up -d

down: 
	docker compose down

cs_docker:
	docker exec -it wallet autoflake . && black . && isort .
