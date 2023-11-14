from pydantic import BaseModel

class SituacaoDoacao(BaseModel):
    id: int
    nome: str