from typing import Dict, List

# Usar dicionário para cache
cache_local: Dict[str, str] = {}
MAX_CACHE_SIZE = 100

# Usar dicionário para cache
historico_chat: List[Dict[str, str]] = []
MAX_HISTORY_MESSAGES = 20


# Recuperar do cache
def recuperar_cache(mensagemm: str) -> str | None:
    return cache_local.get(mensagemm)


# Armazenar no cache
def armazenar_cache(mensagemm: str, resposta: str) -> None:
    if len(cache_local) >= MAX_CACHE_SIZE:
        primeira_chave = next(iter(cache_local))
        cache_local.pop(primeira_chave)
    cache_local[mensagemm] = resposta


# Armazenar no histórico
def adicionar_historico(role: str, content: str) -> None:
    historico_chat.append({"role": role, "content": content})
    if len(historico_chat) > MAX_HISTORY_MESSAGES:
        historico_chat[:] = historico_chat[-MAX_HISTORY_MESSAGES:]


# Obter histórico
def obter_historico() -> List[Dict[str, str]]:
    return historico_chat


# Limpar cache (para testes)
def limpar_cache() -> None:
    cache_local.clear()


# Limpar histórico (para testes)
def limpar_historico() -> None:
    historico_chat.clear()
