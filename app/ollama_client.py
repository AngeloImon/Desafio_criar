import ollama


# Função para interagir com o modelo Llama3 via Ollama
def chat_with_ollama(mensages: list[dict]) -> str:
    response = ollama.chat(model="llama3:8b", messages=mensages)
    print(response)

    return response["message"]["content"]
