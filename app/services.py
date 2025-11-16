from fastapi import HTTPException
from app.logger import logger
from app.ollama_client import chat_with_ollama


def gerar_resposta_local(mensagem: str) -> str:
    try:
        resposta = chat_with_ollama(mensagem)
        return resposta
    except Exception as e:
        logger.error(f"Erro ao gerar resposta local: {e}")
        raise HTTPException(status_code=500, detail="Erro ao gerar resposta local")
