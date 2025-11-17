from app.usecases.chat_usecase import handle_chat
from app.repositories import InMemoryChatRepository
from app.models import ChatPayload
from app.metrics import MedidorPerformance
import asyncio


# Testar handle_chat usecase com mock de serviço
def test_handle_chat_with_mocked_service(monkeypatch):
    repo = InMemoryChatRepository()
    repo.clear()
    repo.clear_history()

    # Mockar gerar_resposta_local para evitar chamar Ollama
    async def fake_gerar_resposta_local(history):
        return "resposta-fake"

    monkeypatch.setattr(
        "app.usecases.chat_usecase.gerar_resposta_local",
        fake_gerar_resposta_local,
        raising=False,
    )

    payload = ChatPayload(mensagem="Teste")
    medidor = MedidorPerformance()

    # Chamar usecase de forma síncrona via asyncio.run
    result = asyncio.run(handle_chat(payload, repo, medidor))

    assert "resposta" in result
    assert result["resposta"] == "resposta-fake"
    assert "metricas" in result
