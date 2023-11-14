import bcrypt
from datetime import datetime

class Utils():
    @classmethod
    def hash_senha(cls, senha:str) -> str:
        # Gere um salt (valor aleatório) para adicionar entropia ao processo de hash
        salt = bcrypt.gensalt()
    
        # Hash da senha usando o salt
        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), salt)
    
        # Retorne o hash gerado (convertido para string)
        return hashed_senha.decode('utf-8')

    @classmethod
    def compararHash(cls, senha_n_cript, senha_cript) -> bool:
        eh_igual= bcrypt.checkpw(password=senha_n_cript.encode("utf-8"), hashed_password=senha_cript.encode("utf-8"))
        # convertida = cls.hash_senha(senha_n_cript)
        if eh_igual:
            return True
        return False
        #Pego a senha criptografada do banco e comparo com a que o user digitou

    @classmethod
    def ativarAlert(cls, mensagem: str, tipo: str) -> dict:
        """
            mensagen: Irá receber a mensagem do corpo do Alert,
            tipo: 'info' | 'sucesso' |'alerta' | 'perigo'
        """
        alert =  {
            "mensagem": mensagem,
            "icone": None,
            "cor": None
        }
        if tipo == "info":
            alert["icone"], alert["cor"] = ("Info:", "primary")
        elif tipo == "sucesso":
            alert["icone"], alert["cor"] = ("Success:", "success")
        elif tipo == "alerta":
            alert["icone"], alert["cor"] = ("Warning:", "warning")
        elif tipo == "perirgo":
            alert["icone"], alert["cor"] = ("Danger:", "danger")

        return alert

    @classmethod
    def formatarDataeHora(cls, date) -> dict:
        """Formato esperado: yyyy-mm-ddThh:mm"""
        
        data_hora_str = date
        data_str, hora_str = data_hora_str.split('T')
        
        data_formatada = datetime.strptime(data_str, '%Y-%m-%d').strftime('%d/%m/%Y')
        hora_formatada = datetime.strptime(hora_str, '%H:%M').strftime('%H:%M')
        
        obj = {'data': data_formatada, 'hora': hora_formatada}
        return obj