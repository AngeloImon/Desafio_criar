from __future__ import annotations
from typing import Dict
from app.models import ChatPayload
from app.repositories import ChatRepository
from app.metrics import MedidorPerformance
from app.services import gerar_resposta_local


async def handle_chat(
    payload: ChatPayload, repo: ChatRepository, medidor: MedidorPerformance
) -> Dict:
    """Orquestra o fluxo do chat: cache -> histórico -> geração -> armazenamento.

    Retorna dicionário com `resposta` e `metricas`.
    """
    # Verifica cache
    cached = repo.get_cache(payload.mensagem)
    if cached:
        return {"resposta": cached, "metricas": {"info": "Resposta obtida do cache"}}

    # Armazenar prompt no histórico
    repo.add_user_message(payload.mensagem)

    # Medir e gerar resposta
    medidor.medir()
    resposta = await gerar_resposta_local(repo.get_history())
    medidor.medir()

    # Persistir
    repo.add_assistant_message(resposta)
    repo.set_cache(payload.mensagem, resposta)

    return {"resposta": resposta, "metricas": medidor.finalizar()}
