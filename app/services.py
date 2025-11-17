import asyncio
from fastapi import HTTPException
from app.logger import logger
from app.ollama_client import chat_with_ollama


# Gerar resposta local usando Ollama (não bloqueante)
async def gerar_resposta_local(mensagem: list[dict]) -> str:
    """Executa a chamada ao client Ollama em um thread worker para não bloquear o
    loop principal do FastAPI.
    """
    # Usar asyncio.to_thread para chamar função bloqueante
    try:
        resposta = await asyncio.to_thread(chat_with_ollama, mensagem)
        return resposta
    except Exception as e:
        logger.error(f"Erro ao gerar resposta local: {e}")
        # Normalizar a exceção para FastAPI
        raise HTTPException(status_code=500, detail="Erro ao gerar resposta local")
