import ollama


def chat_with_ollama(mensagem: str) -> str:
    response = ollama.chat(
        model="llama3:8b", messages=[{"role": "user", "content": mensagem}]
    )
    print(response)

    return response["message"]["content"]
