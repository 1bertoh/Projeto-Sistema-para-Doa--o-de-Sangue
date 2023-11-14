from pydantic import BaseModel


class PublicoUsuario(BaseModel):

    id: int
    nome_completo: str
    cpf: str
    data_nascimento: str
    telefone: str
    telefone_emergencia: str
    email: str
    logradouro: str
    numero: str
    complemento: str
    bairro: str
    cidade: str
    uf: str
    cep: str
    informacao_saude: str
    arquivo_exame: str
    peso: int
    altura: int
    tipo_sangue: str
