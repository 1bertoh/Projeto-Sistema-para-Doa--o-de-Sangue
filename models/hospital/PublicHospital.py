from pydantic import BaseModel

class PublicHospital(BaseModel):
    id: int
    nome: str
    email: str
    localizacao: str
    horario_inicio: str
    horario_fim: str
    segunda: bool
    terca: bool
    quarta: bool
    quinta: bool
    sexta: bool
    sabado: bool
    domingo: bool