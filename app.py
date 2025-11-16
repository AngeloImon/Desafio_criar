from fastapi import FastAPI
from pydantic import BaseModel

# Definir entrada
class ChatPayload(BaseModel):
    message: str

# Definir resposta
class ChatResponse(BaseModel):
    reply: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"teste" : "teste_1"}

@app.post("/chat", response_model=ChatResponse)
def handle_chat(payLoad: ChatPayload):
    # Ecoar a mensagem recebida
    return ChatResponse(reply=f"Você disse: {payLoad.message}")