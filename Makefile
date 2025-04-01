poetry-python:
	source $(poetry env info --path)/bin/activate
start:
	docker compose up
stop:
	docker compose down
image-clean:
	docker image rm bet_maker_app
inside-bet:
	docker exec -it bet_maker_app /bin/sh
format:
	black --config black.toml .
	isort .