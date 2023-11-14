from models.database.Database import Database
from models.hospital.PrivateHospital import PrivateHospital
from models.hospital.PublicHospital import PublicHospital
from typing import List
from fastapi import HTTPException

class HospitalRepo(Database):
    def createTable(self):
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            CREATE TABLE IF NOT EXISTS hospital(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                senha TEXT NOT NULL,
                localizacao TEXT NOT NULL,
                horario_inicio TEXT NOT NULL,
                horario_fim TEXT NOT NULL,
                segunda BOOLEAN NOT NULL,
                terca BOOLEAN NOT NULL,
                quarta BOOLEAN NOT NULL,
                quinta BOOLEAN NOT NULL,
                sexta BOOLEAN NOT NULL,
                sabado BOOLEAN NOT NULL,
                domingo BOOLEAN NOT NULL
            );
        """
        cursor.execute(sql)
        cursor.close()
        self.desconectar()

    def createHospital(self, hospital: PrivateHospital) -> PrivateHospital:
        self.conectar()
        cursor = self.conexao.cursor()
        values = hospital["nome"], hospital["email"], hospital["senha"], hospital["localizacao"], hospital["horario_inicio"], hospital["horario_fim"], hospital["segunda"], hospital["terca"], hospital["quarta"], hospital["quinta"], hospital["sexta"], hospital["sabado"], hospital["domingo"]
        
        sql = """
            INSERT INTO hospital(nome, email, senha, localizacao, horario_inicio, horario_fim, segunda, terca, quarta, quinta, sexta, sabado, domingo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, values)
        self.conexao.commit()
        hospital["id"] = cursor.lastrowid
        cursor.close()
        self.desconectar()

        return hospital

    

    def getHospital(self, id: int) -> PublicHospital:
        self.conectar()
        cursor = self.conexao.cursor()
        sql = """
        SELECT id, nome, email, localizacao, horario_inicio, horario_fim, segunda, terca, quarta, quinta, sexta, sabado, domingo
        FROM hospital
        WHERE id=?
        """

        cursor.execute(sql, (id,))
        resultado = cursor.fetchone()
        if resultado != None :
            hospital_json = {
                "id": resultado[0],"nome": resultado[1], "email": resultado[2], "localizacao": resultado[3], "horario_inicio": resultado[4], "horario_fim": resultado[5], "segunda": resultado[6], "terca": resultado[7], "quarta": resultado[8], "quinta": resultado[9], "sexta": resultado[10], "sabado": resultado[11], "domingo": resultado[12]
            }
            cursor.close()
            self.desconectar()
    
            return hospital_json
        else:
            raise HTTPException(
                status_code=404,
                detail="Hospital não encontrado"
            )

    def getHospitals(self) -> List[PublicHospital]:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            SELECT id, nome, email, localizacao, horario_inicio, horario_fim, segunda, terca, quarta, quinta, sexta, sabado, domingo
            FROM hospital
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        if (resultados is not None):
            
            resultados_json = [
                {
                    "id": r[0],"nome": r[1], "email": r[2], "localizacao": r[3], "horario_inicio": r[4], "horario_fim": r[5], "segunda": r[6], "terca": r[7], "quarta": r[8], "quinta": r[9], "sexta": r[10], "sabado": r[11], "domingo": r[12]
                } for r in resultados
            ]
            cursor.close()
            self.desconectar()
            return resultados_json
        else:
            raise HTTPException(
                status_code=404,
                detail="Hospital não encontrado"
            )

    def updateHospital(self, hospital: PrivateHospital, id: int) -> PrivateHospital:
        self.conectar()
        cursor = self.conexao.cursor()
        values = hospital["nome"], hospital["email"], hospital["senha"], hospital["localizacao"], hospital["horario_inicio"], hospital["horario_fim"], hospital["segunda"], hospital["terca"], hospital["quarta"], hospital["quinta"], hospital["sexta"], hospital["sabado"], hospital["domingo"], id
        
        sql = """
            UPDATE hospital
            SET nome=?, email=?, senha=?, localizacao=?, horario_inicio=?, horario_fim=?, segunda=?, terca=?, quarta=?, quinta=?, sexta=?, sabado=?, domingo=?
            WHERE id=?
        """
        cursor.execute(sql, values)
        self.conexao.commit()
        if cursor.rowcount:
            hospital["id"] = id
            cursor.close()
            self.desconectar()
    
            return hospital
        else:
            raise HTTPException(
                status_code=404,
                detail="Hspital não encontrado"
            )

    def deleteHospital(self, id: int) -> dict:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            DELETE
            FROM hospital
            WHERE id = ?
        """

        cursor.execute(sql , (id,))
        self.conexao.commit()
        if cursor.rowcount:
            cursor.close()
            self.desconectar()
            msg = {"message": "Hospital deletado com sucesso"}
            
            return msg
        else:
            raise HTTPException(
                status_code=404,
                detail="Hospital não encontrado"
            )