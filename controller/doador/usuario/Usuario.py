from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse
from models.hospital.PublicHospital import PublicHospital
from datetime import datetime, time
import os 

class Usuario():
    @classmethod
    async def uploadExameArquivo(cls, arquivo: UploadFile, idUser: int):
        conteudo = await arquivo.read()
        nome_arquivo = f"usuarios-arquivos/user-{idUser}/arquivo_exame.pdf"
    
        if not os.path.exists("usuarios-arquivos"):
            os.makedirs("usuarios-arquivos", exist_ok=True)
    
        if not os.path.exists(f"usuarios-arquivos/user-{idUser}"):
            os.makedirs(f"usuarios-arquivos/user-{idUser}", exist_ok=True)
    
        with open(nome_arquivo, "wb") as f:
            f.write(conteudo)
    
        return {"filename": nome_arquivo}
        #Tratar possiveis erros

    @classmethod
    def getExameArquivo(cls, id:int) -> dict:
        nome_arquivo = f"usuarios-arquivos/user-{id}/arquivo_exame.pdf"
        if os.path.exists(nome_arquivo):
            return {"filename": nome_arquivo}
        else:
            return {"filename": None}

    @classmethod
    def frasesAgendarDoacao(cls, hospital: PublicHospital):
        dias = []
        dias.append("segunda-feira") if hospital["segunda"] else None
        dias.append("terça-feira") if hospital["terca"] else None
        dias.append("quarta-feira") if hospital["quarta"] else None
        dias.append("quinta-feira") if hospital["quinta"] else None
        dias.append("sexta-feira") if hospital["sexta"] else None
        dias.append("sábado") if hospital["sabado"] else None
        dias.append("domingo") if hospital["domingo"] else None

        frase_dias_semana = "Dias da semana válido(s)"+' | '.join(dias)
        frase_horarios = "Das {} ás {}".format(hospital["horario_inicio"], hospital["horario_fim"])

        return {
            "dias": frase_dias_semana,
            "horarios": frase_horarios
        }

    @classmethod
    def checkDataAgendarDoacao(cls, hospital: PublicHospital, data:str):
        dias_permitidos = []
        dias_permitidos.append(0) if hospital["segunda"] else None
        dias_permitidos.append(1) if hospital["terca"] else None
        dias_permitidos.append(2) if hospital["quarta"] else None
        dias_permitidos.append(3) if hospital["quinta"] else None
        dias_permitidos.append(4) if hospital["sexta"] else None
        dias_permitidos.append(5) if hospital["sabado"] else None
        dias_permitidos.append(6) if hospital["domingo"] else None

        arr_data = data.split("T")
        dia = arr_data[0]
        horario = arr_data[1]

        data = datetime.strptime(dia, "%Y-%m-%d")

        if data.weekday() in dias_permitidos:
            pass
        else:
            return {"bool": False, "mensagem": "O dia escolhido é inválido!"}
        horario_inicio = hospital["horario_inicio"].split(":")
        horario_fim = hospital["horario_fim"].split(":")
        horario_escolhido_ = horario.split(":")
        
        horario_inicial = time(int(horario_inicio[0]), int(horario_inicio[1]))
        horario_final = time(int(horario_fim[0]), int(horario_fim[1]))
        
        horario_escolhido = time(int(horario_escolhido_[0]), int(horario_escolhido_[1]))
        
        if horario_inicial <= horario_escolhido <= horario_final:
            pass
        else:
            return {"bool": False, "mensagem": "Horário escolhido está fora do intervalo aceito!"}

        return {"bool": True, "mensagem": "Tudo Ok"}
            