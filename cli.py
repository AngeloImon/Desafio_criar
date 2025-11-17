import requests
import sys

# URL da API FastAPI
API_URL = "http://127.0.0.1:8000/chat"


# Função para enviar mensagem à API e exibir a resposta
def enviar_mensagem(mensagem: str) -> str:
    try:
        response = requests.post(API_URL, json={"mensagem": mensagem})
        if response.status_code == 200:
            data = response.json()
            # Compatibilidade com diferentes formatos de chave
            resposta = data.get("Resposta") or data.get("resposta")
            metricas = data.get("Métricas") or data.get("metricas") or data.get("Metricas")

            print("\n🤖 Resposta:")
            print(resposta, "\n")
            print("\n📊 Métricas:")
            if isinstance(metricas, dict):
                for k, v in metricas.items():
                    print(f" - {k}: {v}")
            else:
                print(" - Nenhuma métrica disponível")
        # Tratar erros da API
        else:
            print(f"Erro {response.status_code}: {response.text}")
    # Tratar erros de conexão
    except Exception as e:
        print(f"Erro ao conectar com a API: {e}")


# Função principal do CLI
def main():
    print("=== CLI Chat com Llama3 ===")
    print("Digite sua mensagem ou 'sair' para encerrar.\n")

    # Loop de interação
    while True:
        try:
            mensagem = input("Você: ")
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando...")
            break
        # Comando para sair
        if mensagem.lower() in ["sair", "exit", "quit"]:
            print("Encerrando...")
            break

        enviar_mensagem(mensagem)


# Execução do CLI
if __name__ == "__main__":
    main()
