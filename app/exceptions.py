class OllamaClientError(Exception):
    """Erro genérico para falhas na comunicação com o cliente Ollama.

    Centraliza o tipo de exceção para facilitar o tratamento em camadas superiores.
    """
    pass
