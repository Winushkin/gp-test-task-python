build:
	docker compose --env-file .env up --build

psql:
	docker compose --env-file .env up --build -d db 
