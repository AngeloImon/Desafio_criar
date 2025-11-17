from typing import Dict, List, Optional
import threading

# Usar dicionário para cache
cache_local: Dict[str, str] = {}
MAX_CACHE_SIZE = 100

# Histórico de chat
historico_chat: List[Dict[str, str]] = []
MAX_HISTORY_MESSAGES = 20

# Locks para segurança em ambiente concorrente
_cache_lock = threading.Lock()
_history_lock = threading.Lock()


# Funções para manipular estado global (cache e histórico)
def recuperar_cache(mensagem: str) -> Optional[str]:
    """Recuperar resposta do cache para a mensagem (thread-safe)."""
    with _cache_lock:
        return cache_local.get(mensagem)


# Armazenar no cache (evita crescimento ilimitado).
def armazenar_cache(mensagem: str, resposta: str) -> None:
    """Armazenar no cache (evita crescimento ilimitado)."""
    with _cache_lock:
        if len(cache_local) >= MAX_CACHE_SIZE:
            primeira_chave = next(iter(cache_local))
            cache_local.pop(primeira_chave)
        cache_local[mensagem] = resposta


# Adicionar ao histórico (mantém tamanho máximo).
def adicionar_historico(role: str, content: str) -> None:
    """Adicionar item ao histórico (mantém tamanho máximo)."""
    with _history_lock:
        historico_chat.append({"role": role, "content": content})
        if len(historico_chat) > MAX_HISTORY_MESSAGES:
            historico_chat[:] = historico_chat[-MAX_HISTORY_MESSAGES:]


# Obter histórico atual.
def obter_historico() -> List[Dict[str, str]]:
    """Retornar uma cópia do histórico atual (não-mutável pelo chamador)."""
    with _history_lock:
        return list(historico_chat)


# Limpar cache (para testes/maintenance).
def limpar_cache() -> None:
    """Limpar o cache (para testes/maintenance)."""
    with _cache_lock:
        cache_local.clear()


# Limpar histórico (para testes/maintenance).
def limpar_historico() -> None:
    """Limpar o histórico (para testes/maintenance)."""
    with _history_lock:
        historico_chat.clear()
