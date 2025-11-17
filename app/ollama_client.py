from typing import List, Dict
import ollama
from app.logger import logger
from app.exceptions import OllamaClientError


# Função para chat com Ollama
def chat_with_ollama(messages: List[Dict]) -> str:
    """Chama o serviço Ollama e retorna o conteúdo da mensagem.

    Esta implementação assume que `ollama.chat` retorna um objeto com o
    atributo `message` (ex.: `ChatResponse`) e que `message.content` contém o
    texto da resposta.
    """
    try:
        response = ollama.chat(model="llama3:8b", messages=messages)
        message = getattr(response, "message", None)
        if message is None:
            raise OllamaClientError(
                "Resposta inesperada do Ollama: campo 'message' ausente"
            )
        content = getattr(message, "content", None)
        if content is None:
            raise OllamaClientError(
                "Resposta inesperada do Ollama: campo 'content' ausente"
            )
        return content
    except Exception as exc:
        logger.exception("Erro ao chamar Ollama")
        raise OllamaClientError(str(exc)) from exc


# Função para inicializar o modelo local
def initialize_model(model: str = "llama3:8b", warmup_message: str = "") -> None:
    """Faz uma chamada de aquecimento para validar o modelo local.

    Lança `OllamaClientError` se a resposta não estiver no formato esperado.
    """
    try:
        logger.info(f"Inicializando modelo local: {model}")
        response = ollama.chat(
            model=model, messages=[{"role": "system", "content": warmup_message}]
        )
        message = getattr(response, "message", None)
        content = getattr(message, "content", None) if message is not None else None
        if not content:
            raise OllamaClientError("Resposta inesperada ao inicializar o modelo")
        logger.info("Modelo inicializado com sucesso")
    except Exception as exc:
        logger.exception("Falha ao inicializar o modelo local")
        raise OllamaClientError(str(exc)) from exc
