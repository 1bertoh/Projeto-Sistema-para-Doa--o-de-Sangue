from models.database.Database import Database
from models.usuario.PrivadoUsuario import PrivadoUsuario
from models.usuario.PublicoUsuario import PublicoUsuario
#from app.user.User import User
from fastapi import HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from typing import List
import os
#criar excessoes http 
class UserRepo(Database):
    def createUserTable(self):
        self.conectar()
        
        command = """CREATE TABLE IF NOT EXISTS User(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome_completo text NOT NULL,
            email text NOT NULL,
            senha text NOT NULL,
            telefone INTEGER NOT NULL,
            telefone_emergencia text NOT NULL,
            logradouro INTEGER NOT NULL,
            numero INTEGER NOT NULL,
            complemento TEXT NOT NULL,
            bairro TEXT NOT NULL,
            cidade INTEGER NOT NULL,
            uf INTEGER NOT NULL,
            cep INTEGER NOT NULL,
            data_nascimento TEXT NOT NULL,
            cpf TEXT NOT NULL,
            informacao_saude TEXT NOT NULL,
            arquivo_exame TEXT NOT NULL,
            peso float NOT NULL,
            altura float NOT NULL,
            tipo_sangue NOT NULL
        );"""

        cursor = self.conexao.cursor()
        cursor.execute(command)
        cursor.close()
        self.desconectar()
        
    def getUsers(self) -> List[PublicoUsuario]:
        self.conectar()
        cursor = self.conexao.cursor()

        command = """
            SELECT id, nome_completo, email, telefone, telefone_emergencia, logradouro, numero, complemento, bairro, cidade, uf, cep, data_nascimento, cpf, informacao_saude, arquivo_exame, peso, altura, tipo_sangue
            FROM User
        """
        cursor.execute(command)

        resultados = cursor.fetchall()
        
        user_json = [
        {    
            "id": u[0], "nome_completo": u[1], "email": u[2], "telefone": u[3], "telefone_emergencia": u[4], "logradouro": u[5], "numero": u[6], "complemento": u[7], "bairro": u[8], "cidade": u[9], "uf": u[10], "cep": u[11], "data_nascimento": u[12], "cpf": u[13], "informacao_saude": u[14], "arquivo_exame": u[15], "peso": u[16], "altura": u[17], "tipo_sangue": u[18]
        } for u in resultados]

        cursor.close()
        self.desconectar()
        return user_json
    
    def getUser(self, id: str) -> PublicoUsuario:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            SELECT id, nome_completo, email, telefone, telefone_emergencia, logradouro, numero, complemento, bairro, cidade, uf, cep, data_nascimento, cpf, informacao_saude, arquivo_exame, peso, altura, tipo_sangue
            FROM User
            Where id=?
        """

        cursor.execute(sql, (id,))
        user = cursor.fetchone()
        
        if user == None:
           raise HTTPException(
               status_code=404,
               detail="User not found"
           )
        else:
            user_json = {    
                "id": user[0], "nome_completo": user[1], "email": user[2], "telefone": user[3], "telefone_emergencia": user[4], "logradouro": user[5], "numero": user[6], "complemento": user[7], "bairro": user[8], "cidade": user[9], "uf": user[10], "cep": user[11], "data_nascimento": user[12], "cpf": user[13], "informacao_saude": user[14], "arquivo_exame": user[15], "peso": user[16], "altura": user[17], "tipo_sangue": user[18]
            }
            cursor.close()
            self.desconectar()
            return user_json
 
    def createUser(self, user: PrivadoUsuario):
        self.conectar()
        cursor = self.conexao.cursor()
        params = user["nome_completo"], user["email"], user["senha"], user["telefone"], user["telefone_emergencia"], user["logradouro"], user["numero"], user["complemento"], user["bairro"], user["cidade"], user["uf"], user["cep"], user["data_nascimento"], user["cpf"], user["informacao_saude"], user["arquivo_exame"], user["peso"], user["altura"], user["tipo_sangue"]
            
        command = """
            INSERT INTO User(nome_completo, email, senha, telefone, telefone_emergencia, logradouro, numero, complemento, bairro, cidade, uf, cep, data_nascimento, cpf, informacao_saude, arquivo_exame, peso, altura, tipo_sangue)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(command, params)
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=400,
                detail="Erro ao cadastrar o usuario"
            )
        user["id"] = cursor.lastrowid
        self.conexao.commit()
        self.conexao.close()
        self.desconectar()
        return user

    async def uploadExameArquivo(self, arquivo: UploadFile, idUser: int):
        conteudo = await arquivo.read()
        nome_arquivo = f"doador/usuarios-arquivos/user-{idUser}/arquivo_exame.pdf"
    
        if not os.path.exists("doador/usuarios-arquivos"):
            os.makedirs("doador/usuarios-arquivos", exist_ok=True)
    
        if not os.path.exists(f"doador/usuarios-arquivos/user-{idUser}"):
            os.makedirs(f"doador/usuarios-arquivos/user-{idUser}", exist_ok=True)
    
        with open(nome_arquivo, "wb") as f:
            f.write(conteudo)

        self.updateExame(idUser, "True")
    
        return {"filename": nome_arquivo}
        #Tratar possiveis erros
    
    def getExameArquivo(self, id:int, ) -> FileResponse:
        nome_arquivo = f"doador/usuarios-arquivos/user-{id}/arquivo_exame.pdf"
        if os.path.exists(nome_arquivo):
            return {"filename": nome_arquivo}
        else:
            raise HTTPException(
                status_code=404,
                detail="Arquivo não encontrado"    
            )
    
    def updateUser(self, id: int, user: PublicoUsuario) -> PublicoUsuario:
        self.conectar()
        cursor = self.conexao.cursor()

        values = user.nome_completo, user.email, user.telefone, user.telefone_emergencia, user.logradouro, user.numero, user.complemento, user.bairro, user.cidade, user.uf, user.cep, user.data_nascimento, user.cpf, user.informacao_saude, user.arquivo_exame, user.peso, user.altura, user.tipo_sangue, id
        sql = """
            UPDATE User
            SET 
            nome_completo=?, email=?, telefone=?, telefone_emergencia=?, logradouro=?, numero=?, complemento=?, bairro=?, cidade=?, uf=?, cep=?, data_nascimento=?, cpf=?, informacao_saude=?, arquivo_exame=?, peso=?, altura=?, tipo_sangue=?
            
            WHERE id=?
        """

        cursor.execute(sql, values)
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="User not Found"
            )
        self.conexao.commit()
        user.id = id
        cursor.close()
        self.desconectar()
        
        return user
    
    def updateExame(self, id: int, msg:str) -> True:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            UPDATE User
            SET 
            arquivo_exame=?
            
            WHERE id=?
        """

        cursor.execute(sql, (msg, id))
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="User not Found"
            )
        self.conexao.commit()
        cursor.close()
        self.desconectar()
        
        return True

    def deleteUser(self, id: int) -> dict:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            DELETE 
            FROM user
            WHERE id = ?
        """
        cursor.execute(sql, (id,))
        self.conexao.commit()
        cursor.close()
        self.desconectar()
        msg = {"message": "Usuário apagado com sucesso"}

        return msg

    def login(self, email: str, senha: str) -> PublicoUsuario:
        self.conectar()
        cursor = self.conexao.cursor()

        sql = """
            SELECT id, nome_completo, email, telefone, telefone_emergencia, logradouro, numero, complemento, bairro, cidade, uf, cep, data_nascimento, cpf, informacao_saude, arquivo_exame, peso, altura, tipo_sangue
            FROM User
            Where email=? AND senha=?
        """

        cursor.execute(sql, (email, senha))
        user = cursor.fetchone()
        
        if user == None:
           raise HTTPException(
               status_code=404,
               detail="Usuário não encontrado"
           )
        else:
            user_json = {    
                "id": user[0], "nome_completo": user[1], "senha": user[2], "telefone": user[3], "telefone_emergencia": user[4], "logradouro": user[5], "numero": user[6], "complemento": user[7], "bairro": user[8], "cidade": user[9], "uf": user[10], "cep": user[11], "data_nascimento": user[12], "cpf": user[13], "informacao_saude": user[14], "arquivo_exame": user[15], "peso": user[16], "altura": user[17], "tipo_sangue": user[18]
            }
            cursor.close()
            self.desconectar()
            return user_json