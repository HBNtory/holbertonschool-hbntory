# HBNtory README


## database service (MySQL)

Be sure to have your `.env` file at the root project with your credentials.

### 1. Start the database
Launch the container in background with the following command:
```bash
docker-compose up -d
```

### 2. Connect with CLI:
Connect as root:
```bash
docker-compose exec db mysql -u root -p
```
Connect as app user
```bash
docker-compose exec db mysql -u hbntory_app -p hbntory
```
*(💡 Adding “hbntory” at the end of this command connects you directly to the correct database.)*

### 3. Stop the database:
```bash
docker-compose down
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