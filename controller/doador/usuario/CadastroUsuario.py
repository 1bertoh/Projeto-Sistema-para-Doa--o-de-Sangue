from fastapi import Form, Request
from models.usuario.UsuarioRepo import UserRepo
from models.usuario.PrivadoUsuario import PrivadoUsuario
from controller.Utils import Utils

class CadastroUsuario():
    etapa = 1
    campos_recebidos={
        "id": 0,
        "nome_completo": "",
        "cpf": "",
        "data_nascimento": "",
        "telefone": "",
        "telefone_emergencia": "",
        "email": "",
        "senha": "",
        "conf_senha": "",
        "logradouro": "",
        "numero": "",
        "complemento": "",
        "bairro": "",
        "cidade": "",
        "uf": "",
        "cep": "",
        "informacao_saude": "",
        "arquivo_exame": "",
        "peso": 0.0,
        "altura": 0.0,
        "tipo_sangue": "",
        "arquivo_conteudo": None
    }
    
    @classmethod
    def checkEtapa(cls):
        if cls.etapa == 1:
            return cls.carregarEtapa1()
        elif cls.etapa == 2:
            return cls.carregarEtapa2()
        elif cls.etapa == 3:
            return cls.carregarEtapa3()
        elif cls.etapa == 4:
            return cls.carregarEtapa4()
        elif cls.etapa == 5:
            return cls.carregarEtapa5()

    @classmethod
    def carregarEtapa1(cls):
        campos = cls.campos_recebidos
        fields = {
            "nome_completo": campos["nome_completo"],
            "cpf": campos["cpf"],
            "data_nascimento": campos["data_nascimento"],
            "telefone": campos["telefone"],
            "telefone_emergencia": campos["telefone_emergencia"],
            "email": campos["email"],
            "senha": campos["senha"]
        }
        return fields
    @classmethod
    def carregarEtapa2(cls):
        campos = cls.campos_recebidos
        fields = {
            "logradouro": campos["logradouro"],
            "numero": campos["numero"],
            "complemento": campos["complemento"],
            "bairro": campos["bairro"],
            "cidade": campos["cidade"],
            "uf": campos["uf"],
            "cep": campos["cep"]
        }
        return fields

    @classmethod
    def carregarEtapa3(cls):
        campos = cls.campos_recebidos
        fields = {
            "informacao_saude": campos["informacao_saude"],
            "arquivo_exame": campos["arquivo_exame"]
        }
        return fields

    @classmethod
    def carregarEtapa4(cls):
        campos = cls.campos_recebidos
        fields = {
            "peso": campos["peso"],
            "altura": campos["altura"],
            "tipo_sangue": campos["tipo_sangue"]
        }
        return fields

    @classmethod
    def carregarEtapa5(cls):
        return {}
    
    @classmethod
    async def receberCampos(cls, campos: Request):
        form = await campos.form()
        chaves = form.keys()
        valores = form.values()
        for chave, valor in zip(chaves, valores):
            cls.campos_recebidos[chave] = valor
        
    @classmethod
    def proximaEtapa(cls):
        cls.etapa += 1

    @classmethod
    def voltarEtapa(cls):
        cls.etapa -= 1

    @classmethod
    def finalizarCadastro(cls):
        user = UserRepo()
        campos = cls.campos_recebidos
        campos["senha"] = Utils.hash_senha(campos["senha"])
        
        user.createUser(campos)