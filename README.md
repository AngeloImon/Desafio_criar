# Desafio Grupo Criar - Chat Local com Llama3

Este projeto fornece uma FastAPI integrada ao Llama3 via Ollama (local), com cache em memória, histórico de conversa e medição de desempenho (CPU/GPU/mem). incluí também um pequeno CLI para testes.

**Instruções de Instalação**

Requisitos (Software):
- Python (versão testada 3.14).
- Ollama (versão testada `3:8b-instruct`).

1. Clone o repositório e entre na pasta do projeto.
2. Crie e ative um ambiente virtual (Windows PowerShell):

```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
```

3. Instale as dependências:

```powershell
pip install -r requirements.txt
```

Observação: algumas dependências como `pynvml` / drivers NVIDIA são opcionais e só são necessárias se quiser métricas de GPU.

**Comando para executar o servidor**

Rode o servidor FastAPI com Uvicorn:

```powershell
uvicorn main:app --reload
```

Isso expõe a API em `http://127.0.0.1:8000`. A documentação automática do FastAPI fica em `/docs` e `/redoc`.

**Exemplo de requisição (curl / HTTPie)**

Usando `curl`:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"mensagem": "Olá, como você está?"}'
```

Usando `http` (HTTPie):

```bash
http POST http://127.0.0.1:8000/chat mensagem="Olá, como você está?"
```

Resposta esperada (exemplo):

```json
{
  "resposta": "Olá! Eu estou bem...",
  "metricas": {
    "tempo_total_segundos": 0.12,
    "cpu_media_percent": 5.2,
    "memoria_media_percent": 40.1,
    "gpu_media_percent": "Sem GPU NVIDIA.",
    "amostras_coletadas": 3
  }
}
```

**Dica — como carregar o modelo local (Ollama)**

Este projeto necessita do Ollama local (daemon/CLI) instalado e um modelo carregado (por exemplo `llama3:8b`).
Passos gerais:

1. Instale o Ollama seguindo as instruções oficiais: https://ollama.com/
2. No terminal com Ollama instalado, baixe/puxe o modelo desejado, por exemplo:

```powershell
ollama pull llama3:8b
```

3. Inicie o serviço Ollama local (pelo app ou CLI). O servidor padrão responde em `http://127.0.0.1:11434` — o cliente Python `ollama` usado aqui fará as chamadas automaticamente.

4. Verifique que o modelo está disponível antes de iniciar o app. Você pode testar com o cliente `ollama` ou observando logs quando iniciar o servidor da API.

**Testes**

Rode os testes unitários:

```powershell
pytest -q
```

**Observações finais**

- O estado atual usa armazenamento em memória (`InMemoryChatRepository`) — para produção, troque por Redis ou outro backend persistente, caso queira.
- O código assume que o `ollama` está instalado e que o modelo retorna `response.message.content` (forma usada pelo cliente atual).