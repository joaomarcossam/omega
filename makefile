start-omega:
	python main.py

server: start-server
	
start-server:
	@echo starting server
	uvicorn server:app --reload

build-postgres: docker/postgres-compose.yml
	docker-compose -f docker/postgres-compose.yml up --build -d
