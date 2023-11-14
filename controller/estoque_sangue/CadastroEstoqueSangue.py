from fastapi import Request
from models.estoque_sangue.EstoqueSangueRepo import EstoqueSangueRepo

class CadastroEstoqueSangue():
    campos_recebidos={
        "id": 0,
        "id_hospital": 0,
        "type_a": 0,
        "type_b": 0,
        "type_ab": 0,
        "type_o": 0,
        "type_a_neg": 0,
        "type_b_neg": 0,
        "type_ab_neg": 0,
        "type_0_neg": 0,
    }

    @classmethod
    def carregarCampos(cls):
        campos = cls.campos_recebidos
        fields = {
            "id_hospital": campos["id_hospital"],
            "type_a": campos["type_a"],
            "type_b": campos["type_b"],
            "type_ab": campos["type_ab"],
            "type_o": campos["type_o"],
            "type_a_neg": campos["type_a_neg"],
            "type_b_neg": campos["type_b_neg"],
            "type_ab_neg": campos["type_ab_neg"],
            "type_o_neg": campos["type_o_neg"],
        }
        return fields
    
    @classmethod
    async def receberCampos(cls, campos: Request):
        form = await campos.form()
        chaves = form.keys()
        valores = form.values()
        for chave, valor in zip(chaves, valores):
            try:
                cls.campos_recebidos[chave] = int(valor)
            except ValueError:
                cls.campos_recebidos[chave] = valor

    @classmethod
    def finalizarCadastro(cls):
        estoque = EstoqueSangueRepo()
        campos = cls.campos_recebidos
        estoque.createEstoqueSangue(campos)

    @classmethod
    def finalizarEdicao(cls):
        estoque = EstoqueSangueRepo()
        campos = cls.campos_recebidos
        id_hospital = campos["id_hospital"]
        estoque.updateEstoqueSangueByHospital(id_hospital, campos)