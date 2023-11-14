from models.database.Database import Database
from models.situacao_doacao.SituacaoDoacao import SituacaoDoacao
from typing import List
from fastapi.exceptions import HTTPException

class SituacaoDoacaoRepo(Database):
    def createTable(self):
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            CREATE TABLE IF NOT EXISTS situacao_doacao(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        """
        cursor.execute(sql)
        cursor.close()
        self.desconectar()

    def createDoacao(self, situacao: SituacaoDoacao) -> SituacaoDoacao:
        self.conectar()
        cursor = self.conexao.cursor()
        values = situacao.nome,
        
        sql = """
            INSERT INTO situacao_doacao( nome)
            VALUES( ?)
        """
        cursor.execute(sql, values)
        self.conexao.commit()
        situacao.id = cursor.lastrowid
        cursor.close
        self.desconectar()

        return situacao

    def getSituacoes(self) -> List[SituacaoDoacao]:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            SELECT id, nome
            FROM situacao_doacao
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        if res is not None:
            res_json = [
                {
                    "id":r[0], "nome":r[1]
                } for r in res
            ]
            cursor.close()
            self.desconectar()
            return res_json

        else:
            raise HTTPException(
                status_code=404,
                detail="Situações não encontrada"
            )

    def getSituacaoFilter(self, id: int=None, nome:str=None) -> SituacaoDoacao:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            SELECT id, nome
            FROM situacao_doacao
            WHERE 1=1
        """

        params = []
        
        if id is not None:
            sql += ' AND id=?'
            params.append(id)
        elif nome is not None:
            sql += ' AND nome=? '
            params.append(nome)

        cursor.execute(sql, params)
        res = cursor.fetchone()
        if res is not None:
            res_json = {
                    "id":res[0], "nome":res[1]
                }
            cursor.close()
            self.desconectar()
            return res_json

        else:
            raise HTTPException(
                status_code=404,
                detail="Stuações não encontrada"
            )
            return False
            
    def atualizarSituacao(self, situacao:SituacaoDoacao, id:int) -> SituacaoDoacao:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            UPDATE situacao_doacao
            SET nome=?
            WHERE id=?
        """
        cursor.execute(sql, (situacao.nome, id))
        self.conexao.commit()
        if cursor.rowcount:
            cursor.close()
            self.desconectar()
            return situacao
        else:
            raise HTTPException(
                status_code=404,
                detail="Situação não encontrada"
            )
    
    def deleteSituacao(self, id:int) -> dict:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            DELETE 
            FROM situacao_doacao
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
                detail="Situacao não encontrada"
            )
            