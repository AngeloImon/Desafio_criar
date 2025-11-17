# Grupo Criar Challenge - Local Chat with Llama3 [PT-BR](https://github.com/AngeloImon/Desafio_criar/blob/main/README.md)

This project provides a FastAPI application that integrates a Llama3 model via Ollama (local), with in-memory caching, conversation history, and performance measurement (CPU/GPU/memory). A small CLI is also included for quick testing.

**Installation Instructions**

Requirements (software):
- Python (tested on 3.14)
- Ollama (tested with model `llama3:8b`)

1. Clone the repository and navigate into the project folder.
2. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

Note: Some dependencies such as `pynvml` / NVIDIA drivers are optional and only required if you want GPU metrics.

**Command to run the server**

Start the FastAPI server with Uvicorn:

```powershell
uvicorn main:app --reload
```

This exposes the API at `http://127.0.0.1:8000`. Auto-generated documentation is available at `/docs` and `/redoc`.

**Example request (curl / HTTPie)**

Using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"mensagem": "Hello, how are you?"}'
```

Using `http` (HTTPie):

```bash
http POST http://127.0.0.1:8000/chat mensagem="Hello, how are you?"
```

Example response:

```json
{
  "resposta": "Hello! I'm doing well...",
  "metricas": {
    "tempo_total_segundos": 0.12,
    "cpu_media_percent": 5.2,
    "memoria_media_percent": 40.1,
    "gpu_media_percent": "Sem GPU NVIDIA.",
    "amostras_coletadas": 3
  }
}
```

**Tip — loading the local model (Ollama)**

This project expects an Ollama daemon/CLI to be installed locally and a model available (for example `llama3:8b`).
General steps:

1. Install Ollama following the official instructions: https://ollama.com/
2. In a terminal where Ollama is available, pull/download the desired model, for example:

```powershell
ollama pull llama3:8b
```

3. Start the Ollama local service (via the app or CLI). The default server listens at `http://127.0.0.1:11434` — the Python `ollama` client used here will call it automatically.

4. Verify the model is available and responding before starting the API. You can test using the `ollama` client or check the API logs when starting the server.

**Tests**

Run unit tests:

```powershell
pytest -q
```

**Final notes**

- The current implementation stores state in memory (`InMemoryChatRepository`) — for production, replace it with Redis or another persistent backend if desired.
- The code assumes the `ollama` client is installed and that the model returns `response.message.content` (the format used by the current client).
