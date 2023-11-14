from models.usuario.PublicoUsuario import PublicoUsuario
from models.hospital.PublicHospital import PublicHospital
from models.situacao_doacao.SituacaoDoacaoRepo import SituacaoDoacaoRepo
from models.doacao.DoacaoRepo import DoacaoRepo
from fastapi.exceptions import HTTPException

class Doacao():
    @classmethod
    def criarDoacao(self, usuario: PublicoUsuario, hospital: PublicHospital, data ):
        sdr = SituacaoDoacaoRepo()
        doa_repo = DoacaoRepo()
        situacoes = sdr.getSituacoes()
        situacao = next(filter(lambda x: str(x["nome"]).upper() == "pendente".upper(), situacoes), None)
        if situacao is None:
            raise HTTPException(
                status_code=404,
                detail="Houve um erro, não há uma situação inicial, 'pendente' no sistema"
            )
        doacao = {
            "id": 0,
            "observacao": '. ',
            "data_hora": data,
            "id_situacao": situacao["id"],
            "sala": '. ',
            "id_hospital": hospital["id"],
            "id_usuario": usuario["id"]
        }

        res = doa_repo.createDoacao(doacao)
        return res
        