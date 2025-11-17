from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.models import ChatPayload, ChatResponse
from app.metrics import MedidorPerformance, get_medidor
from app.ollama_client import initialize_model, OllamaClientError
from app.repositories import InMemoryChatRepository, ChatRepository
from app.usecases.chat_usecase import handle_chat
from app.logger import logger

# Criar a aplicação FastAPI
app = FastAPI()


# Dependência para repository (in-memory singleton)
_repo_singleton: InMemoryChatRepository | None = None


# Retornar instância singleton do repositório
def get_repository() -> ChatRepository:
    global _repo_singleton
    if _repo_singleton is None:
        _repo_singleton = InMemoryChatRepository()
    return _repo_singleton


# Manipuladores de erro
@app.exception_handler(OllamaClientError)
def handle_ollama_error(request: Request, exc: OllamaClientError):
    logger.error(f"Erro Ollama: {exc}")
    return JSONResponse(
        status_code=502, content={"detail": "Erro ao se comunicar com o modelo local."}
    )


@app.exception_handler(Exception)
def handle_general_error(request: Request, exc: Exception):
    logger.exception("Erro interno")
    return JSONResponse(
        status_code=500, content={"detail": "Erro interno do servidor."}
    )


# Rota raiz
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
        <body style="background-color:#222; color:#eee; font-family:Arial; padding:20px;">
            <h1>Bem-vindo ao Desafio de Lógica do Grupo Criar!</h1>
            <ul>
                <li>Use a rota <a href="http://127.0.0.1:8000/docs#/default/prompt_chat_chat_post" style="color:#9cdcfe;">/chat</a> para interagir com o modelo Llama3.</li>
                <li>Use a rota <a href="http://127.0.0.1:8000/docs#/default/manutencao_maintenance_post" style="color:#9cdcfe;">/maintenance</a> para limpar o cache e o histórico.</li>
                <li>Consulte a documentação automática em <a href="/redoc" style="color:#9cdcfe;">/redoc</a>.</li>
            </ul>
        </body>
    """


# Rota para chat
@app.post("/chat", response_model=ChatResponse)
async def prompt_chat(
    payload: ChatPayload,
    medidor: MedidorPerformance = Depends(get_medidor),
    repo: ChatRepository = Depends(get_repository),
):
    logger.info(f"Prompt: {payload.mensagem}")

    result = await handle_chat(payload, repo, medidor)
    # Retornar resposta e métricas
    return ChatResponse(resposta=result["resposta"], metricas=result.get("metricas"))


# Rota para manutenção
@app.post("/maintenance")
def manutencao(repo: ChatRepository = Depends(get_repository)):
    repo.clear()
    repo.clear_history()
    return {"message": "Cache e histórico limpos com sucesso"}


# Evento de startup
@app.on_event("startup")
def app_startup():
    # Tentar inicializar/validar o modelo Ollama local no startup para falhas antecipadas.
    try:
        initialize_model(warmup_message="Aquecimento do modelo para Desafio Criar")
    except Exception as exc:
        logger.warning(f"Falha ao inicializar modelo na inicialização: {exc}")
