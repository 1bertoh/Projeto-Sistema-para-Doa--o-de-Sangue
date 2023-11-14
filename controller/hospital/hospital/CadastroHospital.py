from fastapi import Form, Request
from models.hospital.HospitalRepo import HospitalRepo
from models.hospital.PrivateHospital import PrivateHospital
from controller.Utils import Utils
from models.hospital.PublicHospital import PublicHospital

class CadastroHospital():
    campos_recebidos={
        "id": 0,
        "nome": "",
        "email": "",
        "senha": "",
        "localizacao": "",
        "horario_inicio": "",
        "horario_fim": "",
        "segunda": "",
        "terca": "",
        "quarta": "",
        "quinta": "",
        "sexta": "",
        "sabado": "",
        "domingo": ""
    }

    @classmethod
    def carregarEtapa1(cls):
        campos = cls.campos_recebidos
        fields = {
            "nome": campos["nome"],
            "email": campos["email"],
            "senha": campos["senha"],
            "localizacao": campos["localizacao"],
            "horario_inicio": campos["horario_inicio"],
            "horario_fim": campos["horario_fim"],
            "segunda": campos["segunda"],
            "terca": campos["terca"],
            "quarta": campos["quarta"],
            "quinta": campos["quinta"],
            "sexta": campos["sexta"],
            "sabado": campos["sabado"],
            "domingo": campos["domingo"]
        }
        return fields
    
    @classmethod
    async def receberCampos(cls, campos: Request):
        form = await campos.form()
        chaves = form.keys()
        valores = form.values()
        for chave, valor in zip(chaves, valores):
            cls.campos_recebidos[chave] = valor

    @classmethod
    def finalizarCadastro(cls):
        user = HospitalRepo()
        campos = cls.campos_recebidos
        campos["senha"] = Utils.hash_senha(campos["senha"])
        
        user.createHospital(campos)

    @classmethod
    def finalizarEdicao(cls, id):
        user = HospitalRepo()
        campos = cls.campos_recebidos
        campos["senha"] = Utils.hash_senha(campos["senha"])
        
        user.updateHospital(campos, id)
        