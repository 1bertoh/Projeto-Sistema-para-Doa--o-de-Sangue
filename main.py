from typing import Annotated, List
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from models.usuario.UsuarioRepo import UserRepo
from models.usuario.PublicoUsuario import  PublicoUsuario
from models.usuario.PrivadoUsuario import PrivadoUsuario
from models.hospital.HospitalRepo import HospitalRepo
from models.hospital.PublicHospital import PublicHospital
from models.estoque_sangue.EstoqueSangueRepo import EstoqueSangueRepo
from models.estoque_sangue.EstoqueSangue import EstoqueSangue
from models.situacao_doacao.SituacaoDoacaoRepo import SituacaoDoacaoRepo
from models.situacao_doacao.SituacaoDoacao import SituacaoDoacao
from models.doacao.DoacaoRepo import DoacaoRepo
from models.doacao.Doacao  import Doacao
from controller.Utils import Utils
from controller.doador.usuario.CadastroUsuario import CadastroUsuario 
from controller.doador.usuario.Usuario import Usuario
from controller.doador.sessao.Sessao import Sessao as SessaoDoador
from controller.hospital.sessao.sessao import Sessao as SessaoHospital
from controller.hospital.hospital.CadastroHospital import CadastroHospital
from controller.estoque_sangue.CadastroEstoqueSangue import CadastroEstoqueSangue
from controller.doador.doacao.Doacao import Doacao as DoacaoController

import os  

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates =  Jinja2Templates(directory="views")

app.add_middleware(SessionMiddleware, secret_key=os.urandom(32))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_repo = UserRepo()
hospital_repo = HospitalRepo()
estoque_sangue_repo = EstoqueSangueRepo()
sessao_doador = SessaoDoador()
sessao_hospital = SessaoHospital()
situacao_doacao_repo = SituacaoDoacaoRepo()
doacao_repo = DoacaoRepo()

user_repo.createUserTable()
hospital_repo.createTable()
estoque_sangue_repo.createTable()
situacao_doacao_repo.createTable()
doacao_repo.createTable()

#------------------------------------------DOADOR--------------------------------------

@app.get("/", response_class=HTMLResponse,  tags=["Home"], include_in_schema=False)
async def root(request: Request):
    context = {"request": request, "rota": "inicio", "sistema": "doador"}
    ses = sessao_doador.verIdPelaSessao(request) 
    if ses["id"] and ses["sistema"]:
        id = ses["id"]
        return RedirectResponse(f"/usuario/{id}")
    return templates.TemplateResponse("doador/index.html", context)


@app.get("/cadastro", response_class=HTMLResponse, tags=["Cadastro"], include_in_schema=False)
async def name(request: Request):
    id = sessao_doador.verIdPelaSessao(request)
    if id:
        pass
        
    fields = CadastroUsuario.checkEtapa()
    etapa = CadastroUsuario.etapa
    voltar = CadastroUsuario.voltarEtapa
    context = {"request": request, "fields": fields, "etapa": etapa, "voltar_etapa": voltar, "rota": "cadastro", "sistema": "doador"}
    #O CHECK ETAPA DEVERÁ RETORNAR O OBJETO DOS CAMPOS
    return templates.TemplateResponse("doador/cadastro_usuario/cadastro_usuario.html", context)

@app.post("/cadastro", response_class=RedirectResponse, tags=["Cadastro "], include_in_schema=False)
async def cadastroPost(req: Request):
    form = await req.form()
    await CadastroUsuario.receberCampos(req)
    btn = form.get("botao")
    if btn == "proximo":
        CadastroUsuario.proximaEtapa()
    elif btn == "voltar":
        CadastroUsuario.voltarEtapa()
    elif btn == "finalizar":
        CadastroUsuario.finalizarCadastro()
        #AQUI FAZER O LOGIN
        return RedirectResponse("/login", status_code=301)
    
    return RedirectResponse(url="/cadastro", status_code=301)
    

@app.get("/login", response_class=HTMLResponse, tags=["Login"], include_in_schema=False)
def login(request: Request):
    context = {"request": request, "rota": "login", "sistema": "doador"}
    return templates.TemplateResponse("doador/login.html", context)

@app.post("/login", response_class=RedirectResponse, tags=["Login"], include_in_schema=False)
async def loginPost(request:Request):
    form = await request.form()
    email = form.get("email")
    senha = form.get("senha")
    usuario = sessao_doador.login(email)
    if usuario:
        senha_correta = Utils.compararHash(senha_n_cript=senha, senha_cript=usuario["senha"])
        if senha_correta:
            ses = sessao_doador.inserirChaveSessao(request, usuario["id"])
        else:
            alert = Utils.ativarAlert("Senha incorreta", "alerta")
            context = {"request": request, "alert": alert, "sistema": "doador"}
            #Senha incorreta
            return templates.TemplateResponse("doador/login.html", context)
        if ses:
            #usuário não existe
            return RedirectResponse("/", status_code=301)
    

@app.get("/sobre", response_class=HTMLResponse, tags=["Sobre"], include_in_schema=False)
def sobre(request: Request):
    context = {"request": request, "rota": "sobre", "sistema": "doador"}
    return templates.TemplateResponse("doador/sobre.html", context)

@app.get("/contato", response_class=HTMLResponse, tags=["Contato"], include_in_schema=False)
def contato(request: Request):
    context = {"request": request, "rota": "contato", "sistema": "doador"}
    return templates.TemplateResponse("doador/contato.html", context)

#LOGADO

@app.post("/usuario/logout", response_class=HTMLResponse, tags=["LOGOUT"], include_in_schema=False)
def logout(req: Request):
    sessao_doador.logout(req)
    return RedirectResponse("/", status_code=301)

@app.get("/usuario/{idUsuario}/arquivo-exame", response_class=HTMLResponse, tags=["User"], include_in_schema=False)
async def exameArquivoForm(request: Request, idUsuario: str):
    usuario = user_repo.getUser(idUsuario)
    nome_arquivo = Usuario.getExameArquivo(idUsuario)
    existe = True if nome_arquivo is not None else False
    context = {"request": request, "arquivo": existe, "titulo": "Upload arquivo", "html": "doador/formularios_usuario/upload-arquivo.html", "usuario": usuario}
    return templates.TemplateResponse("doador/formularios_usuario/base-form.html", context)

@app.post("/usuario/{idUsuario}/arquivo-exame", response_class=RedirectResponse, tags=["User"], include_in_schema=False)
async def postExame(
    idUsuario: str,
    arquivo_exame: UploadFile = File(...)
):
    await user_repo.uploadExameArquivo(arquivo_exame, idUsuario)
    return RedirectResponse("/", status_code=301)


@app.get("/usuario/{idUsuario}", response_class=HTMLResponse, tags=["User-logado"], include_in_schema=False)
def inicio(request:Request, idUsuario:str):
    id = sessao_doador.checkSessao(request, idUsuario)
    if id["bool"]:
        usuario = user_repo.getUser(idUsuario)
        context = {"request": request, "usuario": usuario, "sistema": "doador"}
        return templates.TemplateResponse("doador/usuario_logado/inicio.html", context)
    return RedirectResponse("/", status_code=301)

@app.get("/usuario/{idUsuario}/consultar-banco-sangue", response_class=HTMLResponse, tags=["User-logado"], include_in_schema=False)
def bancoDeSangue(request:Request, idUsuario:str, q:str = None):
    id = sessao_doador.checkSessao(request, idUsuario)
    hospitais = hospital_repo.getHospitals()
    if id["bool"]:
        usuario = user_repo.getUser(idUsuario)
        context = {"request": request, "usuario": usuario, "hospitais": hospitais, "sistema": "doador"}
        if q is not None:
            hospital = hospital_repo.getHospital(q)
            estoque = estoque_sangue_repo.getSangueEstoqueByHospital(hospital["id"])
            context["hospital"] = hospital
            context["estoque"] = estoque
        return templates.TemplateResponse("doador/usuario_logado/banco_sangue.html", context)
    return RedirectResponse("/", status_code=301)

@app.get("/usuario/{idUsuario}/gerenciar-doacoes", response_class=HTMLResponse, tags=["User-logado"], include_in_schema=False)
async def gerenciarDoacoes(request:Request, idUsuario:str, q:str = None, data:str = None):
    id = sessao_doador.checkSessao(request, idUsuario)
    hospitais = hospital_repo.getHospitals()
    if id["bool"]:
        usuario = user_repo.getUser(idUsuario)
        id_situacao_aceito = situacao_doacao_repo.getSituacaoFilter(nome="Pendente")["id"]
        doacoes = await doacao_repo.getDoacoesFilter(id_usuario=idUsuario, id_situacao=id_situacao_aceito)
        context = {"request": request, "usuario": usuario, "hospitais": hospitais, "doacoes": doacoes, "sistema": "doador"}
        if q is not None:
            hospital = hospital_repo.getHospital(q)
            frases = Usuario().frasesAgendarDoacao(hospital)
            context["hospital"] = hospital
            context['frases'] = frases
            context['id_hospital'] = int(q)
            if data:
                res_check = Usuario().checkDataAgendarDoacao(hospital, data)
                context['data'] = data
                data_eh_valida = res_check["bool"]
                if data_eh_valida:
                    DoacaoController().criarDoacao(usuario, hospital, data)
                    return RedirectResponse("/", status_code=301)
                else:
                    context["error"] = res_check
        return templates.TemplateResponse("doador/usuario_logado/gerenciar_doacoes.html", context)
    return RedirectResponse("/", status_code=301)

@app.post("/usuario/solicitacao-doacao/cancelar", response_class=RedirectResponse, tags=["User-Logado"], include_in_schema=False)
async def cancelarDoacao(request: Request):
    form = await request.form()
    id_doador = sessao_doador.verIdPelaSessao(request)["id"]
    ses = sessao_doador.checkSessao(request, id_doador)
    if ses:
        id_solicitacao = form.get("doacao")
        id_solicitacao_cancelado = situacao_doacao_repo.getSituacaoFilter(nome="Cancelado")["id"]
        await doacao_repo.atualizarSituacao(id_solicitacao_cancelado, id_solicitacao)
        return RedirectResponse(f"/usuario/{id_doador}/gerenciar-doacoes", status_code=301)
    return RedirectResponse("/", status_code=301)

@app.get("/usuario/{idUsuario}/historico-doacoes", response_class=HTMLResponse, tags=["User-logado"], include_in_schema=False)
async def historicoDoacoes(request:Request, idUsuario:str, id_hospital:int=None, data_inicio:str=None, data_fim:str=None):
    id = sessao_doador.checkSessao(request, idUsuario)
    if id["bool"]:
        hospitais = hospital_repo.getHospitals()
        usuario = user_repo.getUser(idUsuario)
        context = {"request": request, "doacoes": None, "hospitais": hospitais, "usuario": usuario, "sistema": "doador"}
        context["params"] = {"data_inicio": data_inicio, "data_fim": data_fim, "id_hospital": id_hospital}
        if id_hospital and data_inicio and data_fim:
            doacoes = await doacao_repo.getDoacoesFilter(id_usuario=idUsuario, id_hospital=id_hospital, data_inicio=data_inicio, data_fim=data_fim)
            context["doacoes"] = doacoes
        return templates.TemplateResponse("doador/usuario_logado/historico_doacoes.html", context)
    return RedirectResponse("/", status_code=301)


#-----------------------------------------HOSPITAL---------------------------------

@app.get("/hospital/", response_class=HTMLResponse,  tags=["Hospital-home"], include_in_schema=False)
async def rootHospital(request: Request):
    context = {"request": request, "rota": "inicio", "sistema": "hospital"}
    ses = sessao_hospital.verIdPelaSessao(request)
    if ses["id"] and ses["sistema"]:
        id = ses["id"]
        return RedirectResponse(f"/hospital/{id}")
    elif ses["id"] and not ses["sistema"]:
        return {"message": "no auth"}
    return templates.TemplateResponse("hospital/index.html", context)

@app.post("/hospital/login", response_class=RedirectResponse, tags=["Login"], include_in_schema=False)
async def hospitalLoginPost(request:Request):
    form = await request.form()
    email = form.get("email")
    senha = form.get("senha")
    usuario = sessao_hospital.login(email)
    if usuario:
        senha_correta = Utils.compararHash(senha_n_cript=senha, senha_cript=usuario["senha"])
        if senha_correta:
            ses = sessao_hospital.inserirChaveSessao(request, usuario["id"])
        else:
            alert = Utils.ativarAlert("Senha incorreta", "alerta")
            context = {"request": request, "alert": alert, "sistema": "hospital"}
            #Senha incorreta
            return templates.TemplateResponse("hospital/index.html", context)
        if ses:
            #usuário não existe
            return RedirectResponse("/hospital", status_code=301)

@app.get("/hospital/cadastro", response_class=HTMLResponse, tags=["Hospital-Cadastro"], include_in_schema=False)
async def hospitalCadastro(request: Request):
    ses = sessao_hospital.verIdPelaSessao(request)
    if ses["id"] and ses["sistema"] :
        pass
        
    # fields = CadastroHospital.checkEtapa()
    # etapa = CadastroHospital.etapa
    # voltar = CadastroHospital.voltarEtapa
    context = {"request": request}
    #O CHECK ETAPA DEVERÁ RETORNAR O OBJETO DOS CAMPOS
    return templates.TemplateResponse("hospital/cadastro_hospital/cadastro_hospital.html", context)

@app.post("/cadastrar-hospital", response_class=RedirectResponse, tags=["Hospital-Cadastro "], include_in_schema=False)
async def hospitalCadastroPost(req: Request):
    # form = await req.form()
    await CadastroHospital.receberCampos(req)
    CadastroHospital.finalizarCadastro()
    
    return RedirectResponse("/hospital", status_code=301)
    
    return RedirectResponse(url="/cadastro", status_code=301)

# @app.post("/login-hospital", response_class=RedirectResponse, tags=["Hospital-Login"])
# async def hospitalLoginPost(request:Request):
#     form = await request.form()
#     email = form.get("email")
#     senha = form.get("senha")
#     usuario = sessao_hospital.login(email)
#     if usuario:
#         senha_correta = Utils.compararHash(senha_n_cript=senha, senha_cript=usuario["senha"])
#         if senha_correta:
#             ses = sessao_hospital.inserirChaveSessao(request, usuario["id"])
#         else:
#             alert = Utils.ativarAlert("Senha incorreta", "alerta")
#             context = {"request": request, "alert": alert, "sistema": "hospital"}
#             #Senha incorreta
#             return templates.TemplateResponse("/hospital", context)
#         if ses:
#             #usuário não existe
#             return RedirectResponse("/hospital", status_code=301)

#--------LOGADO---------

@app.post("/hospital/logout", response_class=HTMLResponse, tags=["LOGOUT"], include_in_schema=False)
def logoutHospital(req: Request):
    sessao_hospital.logout(req)
    return RedirectResponse("/hospital", status_code=301)

@app.get("/hospital/{idUsuario}", response_class=HTMLResponse, tags=["Hospital-User-logado"], include_in_schema=False)
def inicioHospital(request:Request, idUsuario:int):
    ses = sessao_hospital.checkSessao(request, idUsuario)
    if ses["bool"]:
        hospital = hospital_repo.getHospital(idUsuario)
        context = {"request": request, "id": idUsuario, "usuario": hospital, "sistema": "hospital"}
        return templates.TemplateResponse("hospital/hospital_logado/inicio.html", context)
    return RedirectResponse("/hospital", status_code=301)

@app.get("/hospital/{idUsuario}/editar/menu", response_class=HTMLResponse, tags=["Hospital-User-logado"], include_in_schema=False)
def editarHospitalMenu(request:Request, idUsuario:int):
    ses = sessao_hospital.checkSessao(request, idUsuario)
    if ses["bool"]:
        context = {"request": request, "id": idUsuario, "sistema": "hospital"}
        return templates.TemplateResponse("hospital/editar_hospital/menu.html", context)
    return RedirectResponse("/hospital", status_code=301)

@app.get("/hospital/{idUsuario}/editar-hospital", response_class=HTMLResponse, tags=["Hospital-User-logado"], include_in_schema=False)
def getEditarHospital(request:Request, idUsuario:int):
    ses = sessao_hospital.checkSessao(request, idUsuario)
    if ses["bool"]:
        hospital = hospital_repo.getHospital(idUsuario)
        context = {"request": request, "id": idUsuario, "hospital": hospital, "sistema": "hospital"}
        return templates.TemplateResponse("hospital/editar_hospital/editar_hospital.html", context)
    return RedirectResponse("/hospital", status_code=301)

@app.post("/hospital/{idUsuario}/editar-hospital", response_class=RedirectResponse, tags=["Hospital-User-logado"], include_in_schema=False)
async def editarHospital(request:Request, idUsuario:int):
    ses = sessao_hospital.checkSessao(request, idUsuario)
    if ses["bool"]:
        await CadastroHospital.receberCampos(request)
        CadastroHospital.finalizarEdicao(idUsuario)
        return RedirectResponse(f"/hospital/{idUsuario}/editar/menu", status_code=301)
    return RedirectResponse("/hospital", status_code=301)

@app.get("/hospital/{idUsuario}/editar-estoque-sangue", response_class=HTMLResponse, tags=["Hospital-User-logado"], include_in_schema=False)
def editarHospitalEstoqueSangue(request:Request, idUsuario:int):
    ses = sessao_hospital.checkSessao(request, idUsuario)
    estoque = estoque_sangue_repo.getSangueEstoqueByHospital(idUsuario)
    if ses["bool"]:
        hospital = hospital_repo.getHospital(idUsuario)
        context = {"request": request, "id": idUsuario, "usuario": hospital, "estoque": estoque,  "sistema": "hospital"}
        if estoque is not None:
            return templates.TemplateResponse("hospital/editar_hospital/editar_estoque_sangue.html", context)
        else:
            return templates.TemplateResponse("hospital/editar_hospital/criar_estoque_sangue.html", context)
        
    return RedirectResponse("/hospital", status_code=301)

@app.post("/hospital/{id_hospital}/cadastrar-estoque-sangue", response_class=RedirectResponse, tags=["Hospital-User-logado"], include_in_schema=False)
async def criarHospitalEstoque(request:Request, id_hospital:int):
    ses = sessao_hospital.checkSessao(request, id_hospital)
    if ses["bool"]:
        await CadastroEstoqueSangue.receberCampos(request)
        CadastroEstoqueSangue.finalizarCadastro()
        
    return RedirectResponse("/hospital", status_code=301)

@app.post("/hospital/{id_hospital}/editar-estoque-sangue", response_class=RedirectResponse, tags=["Hospital-User-logado"], include_in_schema=False)
async def editarHospitalEstoque(request:Request, id_hospital:int):
    ses = sessao_hospital.checkSessao(request, id_hospital)
    if ses["bool"]:
        await CadastroEstoqueSangue.receberCampos(request)
        CadastroEstoqueSangue.finalizarEdicao()
        
    return RedirectResponse("/hospital", status_code=301)

@app.get("/hospital/{idUsuario}/solicitacoes-doacao", response_class=HTMLResponse, tags=["Hospital-User-logado"], include_in_schema=False)
async def solicitacoesDoacao(request: Request, idUsuario: int):
    ses = sessao_hospital.checkSessao(request, idUsuario)
    if ses["bool"]:
        id_situacao_pendente = situacao_doacao_repo.getSituacaoFilter(nome="Pendente")["id"]
        solicitacoes = await doacao_repo.getDoacoesFilter(id_situacao=id_situacao_pendente, id_hospital=idUsuario)
        context = {"request": request, "id": idUsuario, "solicitacoes": solicitacoes, "sistema": "hospital"}
        return templates.TemplateResponse("hospital/solicitacoes_doacao/solicitacoes_doacao.html", context)
    return RedirectResponse("/hospital", status_code=301)

@app.get("/hospital/{idUsuario}/solicitacao-doacao/{id_solicitacao}", response_class=HTMLResponse, tags=["Hospital-User-logado"], include_in_schema=False)
async def solicitacaoDoacao(request: Request, idUsuario: int, id_solicitacao: int):
    ses = sessao_hospital.checkSessao(request, idUsuario)
    if ses["bool"]:
        solicitacao = await doacao_repo.getDoacaoById(id_solicitacao)
        doador = user_repo.getUser(solicitacao["id_usuario"])
        context = {"request": request, "id": idUsuario, "doador": doador, "solicitacao": solicitacao, "sistema": "hospital"}
        return templates.TemplateResponse("hospital/solicitacoes_doacao/solicitacao_doacao.html", context)
    return RedirectResponse("/hospital", status_code=301)

@app.get("/hospital/{idUsuario}/solicitacao-doacao/{id_solicitacao}/aceitar", response_class=HTMLResponse, tags=["Hospital-User-logado"], include_in_schema=False)
async def getAceitarSolicitacaoDoacao(request: Request, idUsuario: int, id_solicitacao: int):
    ses = sessao_hospital.checkSessao(request, idUsuario)
    if ses["bool"]:
        return templates.TemplateResponse("hospital/solicitacoes_doacao/observacao_aceitar.html", {"request": request, "id_doacao": id_solicitacao})
    return RedirectResponse("/hospital", status_code=301)


@app.post("/hospital/{idUsuario}/solicitacao-doacao/{id_solicitacao}/aceitar", response_class=RedirectResponse, tags=["Hospital-User-logado"], include_in_schema=False)
async def aceitarSolicitacaoDoacao(request: Request, idUsuario: int, id_solicitacao: int):
    ses = sessao_hospital.checkSessao(request, idUsuario)
    if ses["bool"]:
        form = await request.form()
        observacao = form.get("observacao")
        id_solicitacao_aceito = situacao_doacao_repo.getSituacaoFilter(nome="Aceito")["id"]
        await doacao_repo.atualizarSituacao(id_solicitacao_aceito, id_solicitacao)
        await doacao_repo.atualizarObservacao(observacao, id_solicitacao)
        return RedirectResponse(f"/hospital/{idUsuario}/solicitacoes-doacao", status_code=301)
    return RedirectResponse("/hospital", status_code=301)

@app.get("/hospital/{idUsuario}/solicitacao-doacao/{id_solicitacao}/negar", response_class=HTMLResponse, tags=["Hospital-User-logado"], include_in_schema=False)
async def getNegarSolicitacaoDoacao(request: Request, idUsuario: int, id_solicitacao: int):
    ses = sessao_hospital.checkSessao(request, idUsuario)
    if ses["bool"]:
        return templates.TemplateResponse("hospital/solicitacoes_doacao/observacao_negar.html", {"request": request, "id_doacao": id_solicitacao})
    return RedirectResponse("/hospital", status_code=301)
    
@app.post("/hospital/{idUsuario}/solicitacao-doacao/{id_solicitacao}/negar", response_class=RedirectResponse, tags=["Hospital-User-logado"], include_in_schema=False)
async def negarSolicitacaoDoacao(request: Request, idUsuario: int, id_solicitacao: int):
    ses = sessao_hospital.checkSessao(request, idUsuario)
    if ses["bool"]:
        form = await request.form()
        observacao = form.get("observacao")
        id_solicitacao_aceito = situacao_doacao_repo.getSituacaoFilter(nome="Recusado")["id"]
        await doacao_repo.atualizarSituacao(id_solicitacao_aceito, id_solicitacao)
        await doacao_repo.atualizarObservacao(observacao, id_solicitacao)
        return RedirectResponse(f"/hospital/{idUsuario}/solicitacoes-doacao", status_code=301)
    return RedirectResponse("/hospital", status_code=301)








#-----------------------API-----------------------------------------
#-----------------------Estoque Sangue------------------------------------

@app.get("/estoque-sangue/{id}", response_model=EstoqueSangue, tags=["Estoque-sangue"])
def getEstoque(id:int):
    res = estoque_sangue_repo.getSangueEstoque(id)
    return res

@app.get("/estoque-sangue", response_model=List[EstoqueSangue], tags=["Estoque-sangue"])
def getEstoques():
    res = estoque_sangue_repo.getSangueEstoques()
    return res

@app.post("/estoque-sangue", response_model=EstoqueSangue, tags=["Estoque-sangue"])
def postEstoque(form:EstoqueSangue):
    res = estoque_sangue_repo.createEstoqueSangue(form)
    return res

@app.put("/estoque-sangue/{id}", response_model=EstoqueSangue, tags=["Estoque-sangue"])
def putEstoque(form:EstoqueSangue, id: int):
    res = estoque_sangue_repo.updateEstoqueSangue(id, form)
    return res

@app.delete("/estoque-sangue/{id}", response_model=dict, tags=["Estoque-sangue"])
def deleteEstoque(id:int):
    res = estoque_sangue_repo.deleteEstoqueSangue(id=id)
    return res

@app.delete("/estoque-sangue/hospital/{id}", response_model=dict, tags=["Estoque-sangue"])
def deleteHospitalEstoque(id:int):
    res = estoque_sangue_repo.deleteEstoqueSangue(id_hospital=id)
    return res

# @app.get("/hospital/{idUsuario}/api", response_model=PublicHospital, tags=["Hospital"])
# def getHospital( idUsuario:int):
#     hospital = hospital_repo.getHospital(idUsuario)
#     return hospital

#---------------------------------SITUACOES-------------------------------

@app.get("/situacoes", response_model=List[SituacaoDoacao], tags=["Situacao-doacao"])
def getSituacoes():
    res = situacao_doacao_repo.getSituacoes()
    return res

@app.get("/situacao", response_model=SituacaoDoacao, tags=["Situacao-doacao"])
def getSituacao(id: int = None, nome: str = None):
    res = situacao_doacao_repo.getSituacaoFilter(id=id, nome=nome)
    return res

@app.get("/situacao/{id}/atualizar", response_model=SituacaoDoacao, tags=["Situacao-doacao"])
def atualizarSituacao(id: int, situacao: SituacaoDoacao):
    res = situacao_doacao_repo.atualizarSituacao(id=id, situacao= situacao)
    return res

@app.post("/situacao-doacao", response_model=SituacaoDoacao, tags=["Situacao-doacao"])
def postSituacai(form:SituacaoDoacao):
    res = situacao_doacao_repo.createDoacao(form)
    return res

@app.delete("/situacao/{id}", response_model=dict, tags=["Situacao-doacao"])
def deleteSituacao(id:int):
    res = situacao_doacao_repo.deleteSituacao(id)
    return res

#-----------------------------Doacoes----------------------------

@app.get("/doacoes", response_model=List[Doacao], tags=["Doacoes"])
async def getDoacoes(id_situacao:int=None, id_usuario:int=None, id_hospital:int = None):
    res = await doacao_repo.getDoacoesFilter(id_situacao=id_situacao, id_usuario=id_usuario, id_hospital=id_hospital)
    return res

@app.get("/doacao/{id}", response_model=Doacao, tags=["Doacoes"])
async def getDoacao(id:int):
    res = await doacao_repo.getDoacaoById(id)
    return res

@app.post("/doacoes", response_model=Doacao, tags=["Doacoes"])
def postDoacoes(form:Doacao):
    res = doacao_repo.createDoacao(form)
    return res

@app.post("/doacao/{id_doacao}/observacao/{id_obs}", response_model=Doacao, tags=["Doacoes"])
async def postDoacaoObservacao(id_doacao: int, obs:str):
    res = await doacao_repo.atualizarObservacao(obs, id_doacao)
    return res

@app.post("/doacao/{id}/situacao", response_model=Doacao, tags=["Doacoes"])
async def postDoacaoSituacao(id:int, situacao:int):
    res = await doacao_repo.atualizarSituacao(situacao, id)
    return res


@app.put("/usuario/{id}/editar", response_model=PublicoUsuario, tags=["Doador"])
async def atualizarUsuario(id:int, user:PublicoUsuario):
    res = user_repo.updateUser(id, user)
    return res