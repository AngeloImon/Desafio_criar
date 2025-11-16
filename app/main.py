from fastapi import FastAPI
from app.models import ChatPayload, ChatResponse
from app.services import gerar_resposta_local
from app.logger import logger
from app.state import (
    adicionar_historico,
    armazenar_cache,
    obter_historico,
    recuperar_cache,
    limpar_cache,
    limpar_historico,
)

# Criar a aplicação FastAPI
app = FastAPI()


# Rota raiz para teste
@app.get("/")
def read_root():
    return {"teste": "Desafio Criar"}


# Rota para chat
@app.post("/chat", response_model=ChatResponse)
def prompt_chat(payload: ChatPayload):
    logger.info(f"Prompt: {payload.mensagem}")

    # Cache
    resposta_cache = recuperar_cache(payload.mensagem)
    if resposta_cache:
        logger.info("Resposta obtida do cache:")
        return ChatResponse(resposta=resposta_cache)

    # Histórico
    adicionar_historico("user", payload.mensagem)
    resposta_llama3 = gerar_resposta_local(obter_historico())
    adicionar_historico("assistant", resposta_llama3)

    # Atualizar cache
    armazenar_cache(payload.mensagem, resposta_llama3)

    # Log da resposta
    logger.info(f"Resposta Llama3: {resposta_llama3[:50]}...")
    return ChatResponse(resposta=resposta_llama3)


# Rota para manutenção
@app.post("/maintenance")
def manutencao():
    limpar_cache()
    limpar_historico()
    return {"message": "Cache e histórico limpos com sucesso"}
