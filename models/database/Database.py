import sqlite3

class Database():
    def conectar(self) -> None:
        conexao = sqlite3.connect("db.db")
        self.conexao = conexao

    def desconectar(self):
        self.conexao.close()