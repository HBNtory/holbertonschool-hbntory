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

*Note: if you want to reset everything and delete the saved data, use `docker-compose down -v`*

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
