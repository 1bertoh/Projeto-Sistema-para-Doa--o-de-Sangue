from models.usuario.PrivadoUsuario import PrivadoUsuario
from fastapi import HTTPException, Request
from models.database.Database import Database
from controller.Utils import Utils

class Sessao(Database):
    
    def login(self, email: str) -> PrivadoUsuario:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            SELECT id, nome, email, senha, localizacao, horario_inicio, horario_fim, segunda, terca, quarta, quinta, sexta, sabado, domingo
            FROM hospital
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
                "id": user[0], "nome": user[1], "email": user[2], "senha": user[3], "localizacao": user[4], "horario_inicio": user[5], "horario_fim": user[6], "segunda": user[7], "terca": user[8], "quarta": user[9], "quinta": user[10], "sexta": user[11], "sabado": user[12], "domingo": user[13]
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
            request.session["sistema"] = "hospital"
            return True
        except:
            None

    def checkSessao(self, req:Request, id:  int) -> dict:
        sucesso = {"bool": True, "codigo": 1, "message": "Permissão concedida"}
        falha = {"bool": False, "codigo": 0, "message": "Usuário não logado"}
        no_auth = {"bool": False, "codigo": -1, "message": "Permissão negada"}
        try:
            if req.session["usuario"] == id and req.session["sistema"] == 'hospital':
                return sucesso
            elif req.session["usuario"] == id and req.session["sistema"] != 'hospital':
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