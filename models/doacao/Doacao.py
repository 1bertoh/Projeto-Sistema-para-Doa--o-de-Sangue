from pydantic import BaseModel

class Doacao(BaseModel):
    id: int
    observacao: str 
    data_hora: str
    id_situacao: int
    sala: str 
    id_hospital: int
    id_usuario: int