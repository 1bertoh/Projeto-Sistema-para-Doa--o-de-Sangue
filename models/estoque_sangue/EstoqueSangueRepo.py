from models.database.Database import Database
from models.estoque_sangue.EstoqueSangue import EstoqueSangue
from fastapi.exceptions import HTTPException
from typing import List
class EstoqueSangueRepo(Database):
    def createTable(self):
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            CREATE TABLE IF NOT EXISTS estoque_sangue(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_hospital INT UNIQUE NOT NULL,
            data_atualizacao TEXT NOT NULL,
            type_a INTEGER NOT NULL,
            type_b INTEGER NOT NULL,
            type_ab INTEGER NOT NULL,
            type_o INTEGER NOT NULL,
            type_a_neg INTEGER NOT NULL,
            type_b_neg INTEGER NOT NULL,
            type_ab_neg INTEGER NOT NULL,
            type_o_neg INTEGER NOT NULL,
            FOREIGN KEY(id_hospital) REFERENCES hospital(id)
            )
        """

        cursor.execute(sql)
        cursor.close()
        self.desconectar()

    def createEstoqueSangue(self, estoque: EstoqueSangue) -> EstoqueSangue:
        self.conectar()
        cursor = self.conexao.cursor()

        values = estoque["id_hospital"], estoque["data_atualizacao"], estoque["type_a"], estoque["type_b"], estoque["type_ab"], estoque["type_o"], estoque["type_a_neg"], estoque["type_b_neg"], estoque["type_ab_neg"], estoque["type_o_neg"]

        sql = """
            INSERT INTO estoque_sangue(id_hospital, data_atualizacao, type_a, type_b, type_ab, type_o, type_a_neg, type_b_neg, type_ab_neg, type_o_neg)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(sql, values)
        self.conexao.commit()
        estoque["id"] = cursor.lastrowid
        cursor.close()
        self.desconectar()
        return estoque

    def getSangueEstoque(self, id: int) -> EstoqueSangue:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            SELECT id, id_hospital, data_atualizacao, type_a, type_b, type_ab, type_o, type_a_neg, type_b_neg, type_ab_neg, type_o_neg
            FROM estoque_sangue
            WHERE id=?
        """

        cursor.execute(sql, (id,))
        res = cursor.fetchone()
        if res is not None:
            res_json = {
                "id": res[0], "id_hospital": res[1], "data_atualizacao": res[2], 
                "type_a": res[3], "type_b": res[4], "type_ab": res[5],
                "type_o": res[6], "type_a_neg": res[7], "type_b_neg": res[8],
                "type_ab_neg": res[9], "type_o_neg": res[10]
            }
            cursor.close()
            self.desconectar()
            return res_json
        else:
            raise HTTPException(
                status_code=404,
                detail="Estoque não encontrado"
            )

    def getSangueEstoqueByHospital(self, id_hospital: int) -> EstoqueSangue:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            SELECT id, id_hospital, data_atualizacao, type_a, type_b, type_ab, type_o, type_a_neg, type_b_neg, type_ab_neg, type_o_neg
            FROM estoque_sangue
            WHERE id_hospital=?
        """

        cursor.execute(sql, (id_hospital,))
        res = cursor.fetchone()
        if res is not None:
            res_json = {
                "id": res[0], "id_hospital": res[1], "data_atualizacao": res[2], 
                "type_a": res[3], "type_b": res[4], "type_ab": res[5],
                "type_o": res[6], "type_a_neg": res[7], "type_b_neg": res[8],
                "type_ab_neg": res[9], "type_o_neg": res[10]
            }
            cursor.close()
            self.desconectar()
            return res_json
        else:
            # raise HTTPException(
            #     status_code=404,
            #     detail="Estoque não encontrado"
            # )
            None

    def getSangueEstoques(self) -> List[EstoqueSangue]:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            SELECT id, id_hospital, data_atualizacao, type_a, type_b, type_ab, type_o, type_a_neg, type_b_neg, type_ab_neg, type_o_neg
            FROM estoque_sangue
        """

        cursor.execute(sql)
        resposta = cursor.fetchall()
        if resposta is not None:
            res_json = [
                {
                "id": res[0], "id_hospital": res[1], "data_atualizacao": res[2], 
                "type_a": res[3], "type_b": res[4], "type_ab": res[5],
                "type_o": res[6], "type_a_neg": res[7], "type_b_neg": res[8],
                "type_ab_neg": res[9], "type_o_neg": res[10]
                } for res in resposta
            ]
            cursor.close()
            self.desconectar()
            return res_json

        else:
            raise HTTPException(
                status_code=404,
                detail="Estoques não encontrado"
            )

    def updateEstoqueSangueByHospital(self, id_hospital: int, form: EstoqueSangue) -> EstoqueSangue:
        self.conectar()
        cursor = self.conexao.cursor()
        values = form["id_hospital"], form["data_atualizacao"], form["type_a"], form["type_b"], form["type_ab"], form["type_o"], form["type_a_neg"], form["type_b_neg"], form["type_ab_neg"], form["type_o_neg"], id_hospital
        
        sql = """
            UPDATE estoque_sangue
            SET id_hospital=?, data_atualizacao=?, type_a=?, type_b=?, type_ab=?, type_o=?, type_a_neg=?, type_b_neg=?, type_ab_neg=?, type_o_neg=?
            WHERE id_hospital=?
        """

        # estoque = self.getSangueEstoqueByHospital(id_hospital)
        # id_estoque = estoque.id
        
        cursor.execute(sql, values)
        self.conexao.commit()
        if cursor.rowcount:
            # form.id = id_estoque
            cursor.close()
            self.desconectar()
        else:
            raise HTTPException(
                status_code=404,
                detail="Estoque não encontrado"
            )

    def updateEstoqueSangue(self, id: int, form: EstoqueSangue) -> EstoqueSangue:
        self.conectar()
        cursor = self.conexao.cursor()
        values =  form.type_a, form.data_atualizacao, form.type_b, form.type_ab, form.type_o, form.type_a_neg, form.type_b_neg, form.type_ab_neg, form.type_o_neg, id
        
        sql = """
            UPDATE estoque_sangue
            SET( type_a=?, data_atualizacao=?, type_b=?, type_ab=?, type_o=?, type_a_neg=?, type_b_neg=?, type_ab_neg=?, type_o_neg=?)
            WHERE id=?
        """

        # estoque = self.getSangueEstoqueByHospital(id_hospital)
        # id_estoque = estoque.id
        
        cursor.execute(sql, values)
        self.conexao.commit()
        if cursor.rowcount:
            # form.id = id_estoque
            cursor.close()
            self.desconectar()
        else:
            raise HTTPException(
                status_code=404,
                detail="Estoque não encontrado"
            )

    def deleteEstoqueSangue(self, id=None, id_hospital=None) -> dict:
        self.conectar()
        cursor = self.conexao.cursor()
        sql = ""
        
        if id is not None:
            sql = """
                DELETE FROM estoque_sangue
                WHERE id=?
            """
            cursor.execute(sql, (id,))
        elif id_hospital is not None:
            sql = """
                DELETE FROM estoque_sangue
                WHERE id_hospital=?
            """
            cursor.execute(sql, (id_hospital,))

        self.conexao.commit()
        if cursor.rowcount:
            cursor.close()
            self.desconectar()
            
            return {"message": "Estoque apagado com sucessi"}
        else:
            raise HTTPException(
                status_code=404,
                detail="Estoque não encontrado"
            )