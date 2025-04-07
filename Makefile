BET-MAKER=bet_maker
export PYTHONPATH := $(PWD):$(PWD)/$(BET-MAKER)

start:
	@ sudo chown -R 1000:1000 docker/*
	@ if [ ! -d "docker/data/db" ]; then \
	    mkdir -p docker/data/db/data && \
	    mkdir -p docker/data/db/backup; \
	fi
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
test:
	export PYTHONPATH=$(PWD)/$(BET-MAKER); \
	python -m pytest $(BET-MAKER)/tests/ -vv