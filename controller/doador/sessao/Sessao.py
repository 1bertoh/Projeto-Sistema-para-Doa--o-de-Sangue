from models.usuario.PrivadoUsuario import PrivadoUsuario
from fastapi import HTTPException, Request
from models.database.Database import Database
from controller.Utils import Utils

class Sessao(Database):
    
    def login(self, email: str) -> PrivadoUsuario:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            SELECT id, nome_completo, email, senha, telefone, telefone_emergencia, logradouro, numero, complemento, bairro, cidade, uf, cep, data_nascimento, cpf, informacao_saude, arquivo_exame, peso, altura, tipo_sangue
            FROM User
            Where email=?
        """

        cursor.execute(sql, (email,))
        user = cursor.fetchone()
        
        if user == None:
           raise HTTPException(
               status_code=404,
               detail="Usuário não encontrado"
           )
        else:
            user_json = {    
                "id": user[0], "nome_completo": user[1], "email": user[2], "senha": user[3], "telefone": user[4], "telefone_emergencia": user[5], "logradouro": user[6], "numero": user[7], "complemento": user[8], "bairro": user[9], "cidade": user[10], "uf": user[11], "cep": user[12], "data_nascimento": user[13], "cpf": user[14], "informacao_saude": user[15], "arquivo_exame": user[16], "peso": user[17], "altura": user[18], "tipo_sangue": user[19]
            }
            cursor.close()
            self.desconectar()
            return user_json

    
    def logout(self, request: Request):
        request.session.pop("usuario")
        request.session.pop("sistema")

    
    def inserirChaveSessao(self, request: Request, id: int) -> bool:
        try:
            request.session["usuario"] = id
            request.session["sistema"] = "doador"
            return True
        except:
            None

    def checkSessao(self, req:Request, id:  str) -> dict:
        sucesso = {"bool": True, "codigo": 1, "message": "Permissão concedida"}
        falha = {"bool": False, "codigo": 0, "message": "Usuário não logado"}
        no_auth = {"bool": False, "codigo": -1, "message": "Permissão negada"}
        try:
            if str(req.session["usuario"]) == id and req.session["sistema"] == "doador":
                return sucesso
            elif str(req.session["usuario"]) == id and not req.session["sistema"] == "doador":
                return no_auth
            return falha
        except KeyError:
            return no_auth

    def verIdPelaSessao(self, req:Request):
        try:
            id = req.session["usuario"]
            sistema = req.session["sistema"]
            return {"id": id, "sistema": sistema}
        except:
            return {
                "id": False,
                "sistema": False
            }