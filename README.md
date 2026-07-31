# HBNtory

## Project Overview

HBNtory is an internal inventory management platform composed of a Flask
Backoffice application, a MySQL database, an AI service and an MCP server.

The platform allows administrators to manage users, branches and stock data.
It also provides AI-assisted queries through the integration of an independent
AI service.

The project is fully containerized using Docker Compose to provide a
reproducible development environment.

## Team Members

- Maxime
- Guillaume
- Rawan

## Architecture Summary

The system is composed of four main services:

     Client
        |
        v
Backoffice (Flask)
        |
+----------------+
|                |
v                v
MySQL      AI Service
                 |
                 v
           MCP Server


### Backoffice

The Backoffice is the main application entry point.

Responsibilities:

- User management
- Branch management
- Stock management
- JWT authentication
- Communication with external services

The application follows a layered architecture:

    Route
      |
      v
    Service
      |
      v
  Repository
      |
      v
  Database


### Database

MySQL stores persistent application data:

- Users
- Branches
- Stock information

### AI Service

The AI service handles AI queries and communicates with the MCP server when
additional information is required.

### MCP Server

The MCP server exposes tools used by the AI service.


## Requirements
- Docker and Docker Compose

## Setup
Copy the environment template and fill in your credentials:
```bash
cp .env.example .env 
```

## Running the services

Start the complete application:

```bash
docker compose up --build
```

Run only the Backoffice:

```bash
docker compose up --build backoffice
```

Run only the AI Service:

```bash
docker compose up --build ai_service
```

Run only the MCP Server:

```bash
docker compose up --build mcp_server
```

Run only the database:

```bash
docker compose up db
```

Stop all services:

```bash
docker compose down
```

## Health check
Once running:
```bash
curl http://localhost:8080/health
```
Expected response: `{"status": "ok", "database": "ok"}`
Returns `503` if the database is unreachable

## Database (MySQL)
Connect as root:
```bash
docker compose exec db mysql -u root -p
```

Connect as the application user (directly on the `hbntory` database):
```bash
docker compose exec db mysql -u <user> -p
```

*Note: if you want to reset everything and delete the saved data, use `docker-compose down -v`*

## Seeding the database

The seed script populates the database with initial data: two branches
(Lille, Paris) and an admin user. It is idempotent — running it several times
will not create duplicates.

### Prerequisites
- The database must be running and healthy.
- The following variables must be set in your `.env`:
```.dotenv
ADMIN_BACKOFFICE_EMAIL=...
ADMIN_BACKOFFICE_PASSWORD=...
```

### Run
From inside the backoffice container (or via `docker compose run`):
```bash
docker compose run --rm backoffice python -m app.scripts.seed
```

The script runs as a module (`-m app.scripts.seed`), not as a file path, so
Python resolves the `app` package correctly.

Expected output on first run: branches and the admin user are created.
On a second run, everything reports "already exists, skipping" (idempotence).


## Ollama

This project uses **Ollama** to run a local AI model.

The AI Query Service depends on Ollama to generate responses. Installing Ollama and downloading a compatible model are **required** to use the AI features.

### Install Ollama

Install Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verify the installation:

```bash
ollama --version
```

### Download a model

Download the model you want to use. For example:

```bash
ollama pull qwen3.5:0.8b
```

### Configure the project

Update the `.env` file so that the `OLLAMA_MODEL` variable matches the downloaded model.

For example:

```env
OLLAMA_MODEL=qwen3.5:0.8b
```

### Start Ollama

Before starting the project, launch the Ollama server:

```bash
ollama serve
```

## Environment variables
See `.env.example` for the full list.

### Generate a JWT secret key

Generate a secure secret key using Python:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Copy the generated value into your `.env` file:

```env
JWT_SECRET_KEY=<your_generated_secret_key>
```

## Authentication

The backoffice uses JWT (JSON Web Token) authentication.

### Login

Authenticate using:

```http
POST /auth/login
```

Request body:

```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

A successful authentication returns a JWT token:

```json
{
  "token": "<jwt_token>"
}
```

Use this token in the `Authorization` header when accessing protected endpoints:

```http
Authorization: Bearer <jwt_token>
```

### Logout

Logout is available through:

```http
POST /auth/logout
```

Because JWT authentication is stateless, the server does not maintain user sessions.

Logging out consists of removing the JWT from the client. A previously issued token remains valid until it expires.

## Accessing the Backoffice

Once the application is running, the Backoffice is available at:

http://localhost:8080

Useful endpoints:

- GET /health
- POST /auth/login
- POST /auth/logout
- /users
- /branches
- /stocks
- /chat

## Main Technical Decisions

### Flask Application Factory

The Backoffice uses Flask's application factory pattern to avoid global state
and simplify testing.

### Layered Architecture

Business logic is separated into routes, services and repositories to keep
responsibilities isolated.

### Argon2 Password Hashing

Passwords are stored using Argon2 hashing to provide secure password storage.

### JWT Authentication

JWT was chosen for authentication because it provides a stateless mechanism
suitable for distributed services.

### AI Communication Through Backoffice

AI requests are routed through the Backoffice instead of exposing the AI
service directly to users.

## Troubleshooting

### Orphan containers warning
If you see a warning about *orphan containers* when starting the stack, it usually comes
from leftover one-off containers (e.g from `docker compose run`).
Clean them up with:
```bash
docker compose down --remove-orphans
```
## Known Limitations

- JWT authentication is stateless; logout only removes the token from the client.
- No token revocation mechanism is implemented.
- Database schema is initialized using SQLAlchemy without migration support.
- Some automated tests are still under development.
