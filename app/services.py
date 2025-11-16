from fastapi import HTTPException
from app.logger import logger
from app.ollama_client import chat_with_ollama


# Gerar resposta local usando Ollama
def gerar_resposta_local(mensagem: list[dict]) -> str:
    # Chama o histórico de mensagens
    try:
        resposta = chat_with_ollama(mensagem)
        return resposta
    # Tratar erros
    except Exception as e:
        logger.error(f"Erro ao gerar resposta local: {e}")
        raise HTTPException(status_code=500, detail="Erro ao gerar resposta local")
