from pydantic import BaseModel

class EstoqueSangue(BaseModel):
    id: int
    id_hospital: int
    data_atualizacao: str
    type_a: int
    type_b: int
    type_ab: int
    type_o: int
    type_a_neg: int
    type_b_neg: int
    type_ab_neg: int
    type_o_neg: int
    