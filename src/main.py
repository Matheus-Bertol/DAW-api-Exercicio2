from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Locacao(BaseModel):
    id: int = "0"
    nome: str
    data_locacao: str
    data_finalizacao: str = "n/a"

locacoes_db = []
IDultimalocacao = 0
quantidadeDeCarros = 10

@app.post("/locacoes", response_model=Locacao)
def nova_locacao(locacao: Locacao):
    global IDultimalocacao
    
    locacao.id = IDultimalocacao + 1
    
    if len(locacoes_db) >= quantidadeDeCarros:
        raise HTTPException(status_code=400, detail=f"Limite de {quantidadeDeCarros} locações atingido! Não é possível adicionar mais locações.")
    else:
        locacoes_db.append(locacao)
        IDultimalocacao += 1
    return locacao