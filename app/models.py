from pydantic import BaseModel


# Definir entrada
class ChatPayload(BaseModel):
    mensagem: str


# Definir resposta
class ChatResponse(BaseModel):
    resposta: str
