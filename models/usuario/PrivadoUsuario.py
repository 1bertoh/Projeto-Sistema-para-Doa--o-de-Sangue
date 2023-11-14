from pydantic import BaseModel

class PrivadoUsuario(BaseModel):

    id: int
    nome_completo: str
    cpf: str
    data_nascimento: str
    telefone: str
    telefone_emergencia: str
    email: str
    senha: str
    logradouro: str
    numero: str
    complemento: str
    bairro: str
    cidade: str
    uf: str
    cep: str
    saude_info: str
    arquivo: str
    peso: int
    altura: int
    tipo_sangue: str
