from app.repositories import InMemoryChatRepository


# Testar InMemoryChatRepository
def test_inmemory_repository_history_and_cache():
    repo = InMemoryChatRepository()

    # limpar estado inicial
    repo.clear()
    repo.clear_history()

    # adicionar mensagem do usuário
    repo.add_user_message("Olá")
    history = repo.get_history()
    assert len(history) == 1
    assert history[0]["role"] == "user"

    # armazenar cache
    repo.set_cache("pergunta", "resposta")
    assert repo.get_cache("pergunta") == "resposta"

    # limpar e garantir remoção
    repo.clear()
    assert repo.get_cache("pergunta") is None
