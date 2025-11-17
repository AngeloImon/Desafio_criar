from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from app import state


class ChatRepository(ABC):
    @abstractmethod
    def add_user_message(self, content: str) -> None:
        pass

    @abstractmethod
    def add_assistant_message(self, content: str) -> None:
        pass

    @abstractmethod
    def get_history(self) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def get_cache(self, prompt: str) -> Optional[str]:
        pass

    @abstractmethod
    def set_cache(self, prompt: str, response: str) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def clear_history(self) -> None:
        pass


class InMemoryChatRepository(ChatRepository):
    """Adapter que delega para as funções em `app.state`.

    Mantém separação de responsabilidades (Repository pattern) e permite trocar
    a implementação por Redis ou outra store sem mudar a camada de serviço.
    """

    def add_user_message(self, content: str) -> None:
        state.adicionar_historico("user", content)

    def add_assistant_message(self, content: str) -> None:
        state.adicionar_historico("assistant", content)

    def get_history(self) -> List[Dict[str, str]]:
        return state.obter_historico()

    def get_cache(self, prompt: str) -> Optional[str]:
        return state.recuperar_cache(prompt)

    def set_cache(self, prompt: str, response: str) -> None:
        state.armazenar_cache(prompt, response)

    def clear(self) -> None:
        state.limpar_cache()

    def clear_history(self) -> None:
        state.limpar_historico()
