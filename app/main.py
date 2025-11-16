from fastapi import FastAPI
from app.models import ChatPayload, ChatResponse
from app.services import gerar_resposta_local
from app.logger import logger

app = FastAPI()


@app.get("/")
def read_root():
    return {"teste": "Desafio Criar"}


@app.post("/chat", response_model=ChatResponse)
def handle_chat(payload: ChatPayload):
    logger.info(f"Prompt: {payload.mensagem}")
    resposta_llama3 = gerar_resposta_local(payload.mensagem)
    logger.info(f"Resposta Llama3: {resposta_llama3}")
    return ChatResponse(resposta=resposta_llama3)
