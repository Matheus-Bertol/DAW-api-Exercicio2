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

# POST /locacoes
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

# GET /locacoes
@app.get("/locacoes", response_model=List[Locacao])
def get_locacoes():
    return locacoes_db

# GET /locacoes/id (locação individual)
@app.get("/locacoes/{locacao_id}", response_model=Locacao)
def get_locacao(locacao_id: int):
    for loc in locacoes_db:
        if loc.id == locacao_id:
            return loc
    raise HTTPException(status_code=404, detail="Locação não encontrada!")

# PUT /locacoes/id (locação individual)
@app.put("/locacoes/{locacao_id}", response_model=Locacao)
def update_locacao(locacao_id: int, locacao: Locacao):
    for loc in locacoes_db:
        if loc.id == locacao_id:
            # Atualize a data de finalização da locação
            loc.data_finalizacao = locacao.data_finalizacao
            return loc
    raise HTTPException(status_code=404, detail="Locação não encontrada!")

# DELETE /locacoes/id

@app.delete("/locacoes/{locacao_id}", status_code=204)
def delete_locacao(locacao_id: int):
    for loc in locacoes_db:
        if loc.id == locacao_id:
            locacoes_db.remove(loc)
            return
    raise HTTPException(status_code=404, detail="Locação não encontrada!")	