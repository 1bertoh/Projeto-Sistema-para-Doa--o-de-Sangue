from models.database.Database import Database
from models.doacao.Doacao import Doacao
from typing import List
from fastapi.exceptions import HTTPException
from models.situacao_doacao.SituacaoDoacaoRepo import SituacaoDoacaoRepo
from models.usuario.UsuarioRepo import UserRepo
from models.hospital.HospitalRepo import HospitalRepo
from controller.Utils import Utils
from datetime import datetime

class DoacaoRepo(Database):

    def __init__(self):
        self.situacao_repo = SituacaoDoacaoRepo()
        self.user = UserRepo()
        self.hospital = HospitalRepo()
        
    
    def createTable(self):
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            CREATE TABLE IF NOT EXISTS doacao(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                observacao TEXT NOT NULL,
                data_hora TEXT NOT NULL,
                id_situacao INTEGER NOT NULL,
                sala TEXT NOT NULL,
                id_hospital INTEGER NOT NULL,
                id_usuario INTEGER NOT NULL,
                FOREIGN KEY(id_situacao) REFERENCES situacao_doacao(id),
                FOREIGN KEY(id_hospital) REFERENCES hospital(id),
                FOREIGN KEY(id_usuario) REFERENCES doacao_usuario(id)
            )
        """
        cursor.execute(sql)
        cursor.close()
        self.desconectar()

    def createDoacao(self, doacao: Doacao) -> Doacao:
        self.conectar()
        cursor = self.conexao.cursor()
        values = doacao["observacao"], doacao["data_hora"], doacao["id_situacao"], doacao["sala"], doacao["id_hospital"], doacao["id_usuario"]
        
        sql = """
            INSERT INTO doacao( observacao, data_hora, id_situacao, sala, id_hospital, id_usuario)
            VALUES(?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, values)
        self.conexao.commit()
        doacao["id"] = cursor.lastrowid
        cursor.close
        self.desconectar()

        return doacao

    def getDoacoes(self) -> List[Doacao]:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            SELECT id, observacao, data_hora, id_situacao, sala, id_hospital, id_usuario
            FROM doacao
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        if res is not None:
            res_json = [
                {
                    "id":r[0], "observacao":r[1], "data_hora":r[2], "id_situacao":r[3],
                    "sala":r[4], "id_hospital":r[5], "id_usuario":r[6]
                } for r in res
            ]
            cursor.close()
            self.desconectar()
            return res_json

        else:
            raise HTTPException(
                status_code=404,
                detail="Doacoes não encontrada"
            )

    async def getDoacaoById(self, id: int) -> Doacao:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            SELECT id, observacao, data_hora, id_situacao, sala, id_hospital, id_usuario
            FROM doacao
            WHERE id=?
        """
        cursor.execute(sql, (id,))
        #Talvez chamar o método da classe situacao para checar se esse id_situacao existe mesmo
        res = cursor.fetchone()
        if res is not None:
            res_json = {
                    "id":res[0], "observacao":res[1], "data_hora":res[2], "id_situacao":res[3],
                    "sala":res[4], "id_hospital":res[5], "id_usuario":res[6]
                }
            cursor.close()
            self.desconectar()
            return res_json

        else:
            raise HTTPException(
                status_code=404,
                detail="Doacao não encontrada"
            )
            
    async def getDoacoesFilter(self, id_situacao: int = None, id_hospital:int = None, id_usuario: int = None, data_inicio: str= None, data_fim: str=None) -> List[Doacao]:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            SELECT id, observacao, data_hora, id_situacao, sala, id_hospital, id_usuario
            FROM doacao
            WHERE 1=1
        """
        params = []
    
        if id_situacao is not None:
            if not self.situacao_repo.getSituacaoFilter(id=id_situacao, nome=None):
                raise HTTPException(
                    status_code=404,
                    detail="ID da situação inválido"
                )
            sql += " AND id_situacao = ? "
            params.append(id_situacao)
    
        if id_hospital is not None:
            sql += " AND id_hospital = ? "
            params.append(id_hospital)
    
        if id_usuario is not None:
            sql += " AND id_usuario = ? "
            params.append(id_usuario)

        if data_inicio is not None and data_fim is not None:
            data_inicio_ = datetime.strptime(data_inicio, '%Y-%m-%dT%H:%M')
            data_fim_ = datetime.strptime(data_fim, '%Y-%m-%dT%H:%M')
            sql += " AND datetime(data_hora) BETWEEN ? AND ? "
            params.append(data_inicio_)
            params.append(data_fim_)
        
        cursor.execute(sql, params)
        res =  cursor.fetchall()
        if res is not None:
            res_json = [
                {
                    "id":r[0], "observacao":r[1], "data_hora":r[2], "id_situacao":r[3],
                    "user": self.user.getUser(r[6]), "data_e_hora": Utils().formatarDataeHora(r[2]), "situacao": self.situacao_repo.getSituacaoFilter(id=r[3]),
                    "sala":r[4], "id_hospital":r[5], "hospital": self.hospital.getHospital(r[5]),  "id_usuario":r[6]
                } for r in res
            ]
            cursor.close()
            self.desconectar()
            return res_json

        else:
            raise HTTPException(
                status_code=404,
                detail="Doacoes não encontrada"
            )

    async def atualizarSituacao(self, id_situacao: int, id:int) -> Doacao:
        self.conectar()
        cursor = self.conexao.cursor()
        if not self.situacao_repo.getSituacaoFilter(id=id_situacao):
            raise HTTPException(
                status_code=404,
                detail="ID da situação inválido"
            )

        sql = """
            UPDATE doacao
            SET id_situacao=?
            WHERE id=?
        """
        cursor.execute(sql, (id_situacao, id))
        self.conexao.commit()
        if cursor.rowcount:
            doacao = await self.getDoacaoById(id)
            cursor.close()
            self.desconectar()
            return doacao
        else:
            raise HTTPException(
                status_code=404,
                detail="Doacao não encontrada"
            )
            
    
    async def atualizarObservacao(self, observacao: str, id:int) -> Doacao:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            UPDATE doacao
            SET observacao=?
            WHERE id=?
        """
        cursor.execute(sql, (observacao, id))
        self.conexao.commit()
        if cursor.rowcount:
            doacao = await self.getDoacaoById(id)
            cursor.close()
            self.desconectar()
            return doacao
        else:
            raise HTTPException(
                status_code=404,
                detail="Doacao não encontrada"
            )
            
    
    def deleteDoacao(self, id:int) -> dict:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            DELETE doacao
            WHERE id=?
        """
        cursor.execute(sql, (id,))
        self.conexao.commit()
        if cursor.rowcount:
            cursor.close()
            self.desconectar()
            return {"mensagem": "Apagado com sucesso!"}
        else:
            raise HTTPException(
                status_code=404,
                detail="Doacao não encontrada"
            )
            