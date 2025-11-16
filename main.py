from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from app.models import ChatPayload, ChatResponse
from app.services import gerar_resposta_local
from app.logger import logger
from app.state import (
    adicionar_historico,
    armazenar_cache,
    obter_historico,
    recuperar_cache,
    limpar_cache,
    limpar_historico,
)
from app.metrics import MedidorPerformance, get_medidor
import time

# Criar a aplicação FastAPI
app = FastAPI()


# Rota raiz
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
        <body style="background-color:#222; color:#eee; font-family:Arial; padding:20px;">
            <h1>Bem-vindo ao Desafio de Lógica do Grupo Criar!</h1>
            <ul>
                <li>Use a rota <a href="http://127.0.0.1:8000/docs#/default/prompt_chat_chat_post" style="color:#9cdcfe;">/chat</a> para interagir com o modelo Llama3.</li>
                <li>Use a rota <a href="http://127.0.0.1:8000/docs#/default/manutencao_maintenance_post" style="color:#9cdcfe;">/maintenance</a> para limpar o cache e o histórico.</li>
                <li>Consulte a documentação automática em <a href="/redoc" style="color:#9cdcfe;">/redoc</a>.</li>
            </ul>
        </body>
    """


# Rota para chat
@app.post("/chat")
def prompt_chat(
    payload: ChatPayload, medidor: MedidorPerformance = Depends(get_medidor)
):
    logger.info(f"Prompt: {payload.mensagem}")

    # Cache
    resposta_cache = recuperar_cache(payload.mensagem)
    if resposta_cache:
        logger.info("Resposta obtida do cache:")
        return {
            "Resposta": resposta_cache,
            "Metricas": {"info": "Resposta obtida do cache, sem medir performance"},
        }

    # Histórico
    adicionar_historico("user", payload.mensagem)
    # Medição de performance
    medidor.medir()
    # Gerar resposta local
    resposta_llama3 = gerar_resposta_local(obter_historico())

    # Simular espera pela resposta
    while not resposta_llama3:
        time.sleep(0.1)
        medidor.medir()
        resposta_llama3 = gerar_resposta_local(obter_historico())
    # Finalizar medição
    medidor.medir()

    # Armazenar no histórico e cache
    adicionar_historico("assistant", resposta_llama3)
    armazenar_cache(payload.mensagem, resposta_llama3)

    # Log da resposta
    logger.info(f"Resposta Llama3: {resposta_llama3[:50]}...")
    return {"Resposta": resposta_llama3, "Métricas": medidor.finalizar()}


# Rota para manutenção
@app.post("/maintenance")
def manutencao():
    limpar_cache()
    limpar_historico()
    return {"message": "Cache e histórico limpos com sucesso"}
