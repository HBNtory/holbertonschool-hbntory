# HBNtory

Internal backoffice service (Flask) for managing users, branches and stock, backed
by a MySQL database. Everything runs through Docker Compose.

## Requirements
- Docker and Docker Compose

## Setup
Copy the environment template and fill in your credentials:
```bash
cp .env.example .env 
```

## Running the services
Start the database and the backoffice:
```bash
docker compose up --build db backoffice
```

Or start everything in the background:
```bash
docker compose up -d
```

Stop the services:
```bash
docker compose down
```
*To reset everything and delete saved data, use `docker compose down -v`*

## Health check
Once running:
```bash
curl http://localhost:8080/health
```
Expected response: `{"status": "ok"}`

## Database (MySQL)
Connect as root:
```bash
docker compose exec db mysql -u root -p
```

Connect as the application user (directly on the `hbntory` database):
```bash
docker compose exec db mysql -u <user> -p <password>
```

## Environment variables
See `.env.example` for the full list.