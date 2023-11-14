import CadastroUsuario from "/static/js/CadastroUsuario.js"

let etapa = 5

let usuario = {}
const cadUsuario = new CadastroUsuario()


//CRIAR UM OBJETO QUE QUE CONTEM AS ETAPAS E A SITUAÇÃO DE PREENCHIMENTO DELAS. 

function consultarEtapa(){
    const form = document.getElementById("form-content")
    form.innerHTML = '' 
    
    switch (etapa){
        case 1:
            etapa1(form);
            break;
        case 2:
            etapa2(form);
            break;
        case 3:
            etapa3(form);
            break;
        case 4:
            etapa4(form);
            break;
        case 5:
            etapa5(form);
            break;
    }    
    
}

window.onload = () => {
    consultarEtapa()    
}


const etapa1 = (form) => {
    const form_conteudo = `
                    <div class="form-floating mb-3">
                        <input type="text" onchange={{cad.nome_completo = }} value="${cadUsuario.nome_completo}" class="form-control" id="nome_completo" name="nome_completo" placeholder="Fulano de Tal">
                        <label for="nome_completo">Nome Completo</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input value="${cadUsuario.cpf}" class="form-control" id="cpf" name="cpf" placeholder="123.456.789-12">
                        <label for="cpf">CPF</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input value="${cadUsuario.data_nascimento}" type="date" class="form-control" id="data_nascimento" name="data_nascimento" placeholder="01/01/2000">
                        <label for="data_nascimento">Data de Nascimento</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input value="${cadUsuario.telefone}" type="tel" class="form-control" id="telefone" name="telefone" placeholder="(28) 99999-9999">
                        <label for="telefone">Telefone</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input value="${cadUsuario.telefone_emergencia}" type="tel" class="form-control" id="telefone_emergencia" name="telefone_emergencia" placeholder="(28) 99999-8888">
                        <label for="telefone_emergencia">Telefone de Emergência</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input value="${cadUsuario.email}" type="email" class="form-control" id="email" name="email" placeholder="fulano@email.com">
                        <label for="email">E-mail</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input value="${cadUsuario.senha}" type="password" class="form-control" id="senha" name="senha" placeholder="123456">
                        <label for="senha">Senha</label>
                    </div>
                    <div class="form-floating">
                        <input value="${cadUsuario.conf_senha}" type="password" class="form-control" id="conf_senha" name="conf_senha" placeholder="123456">
                        <label for="conf_senha">Confirmação de Senha</label>
                    </div>
                    <div class="text-center">
                        <a href="/usuario/cadastro_usuario/registro2.html">
                            <i class="bi bi-arrow-right fs-1 text-white"></i>
                        </a>
                    </div>
                    <div class="d-flex justify-content-between">
                        <span></span>
                        <button type="button" id="etapa1-button-next">Próximo</button>
                    </div>
    `
    form.innerHTML = form_conteudo
    const link1 = document.getElementById("etapa1-link")
    link1.classList.add("active")
    link1.classList.remove("bg-white")
    const btn1 = document.getElementById("etapa1-button-next")

    addEventFunc(["nome_completo", "cpf", "data_nascimento", "telefone", "telefone_emergencia", "email", "senha", "conf_senha"])
    
    btn1.addEventListener("click", () => {
        let  situacao = cadUsuario.getEtapa1()
        
        if(situacao.situacao.bool){
            etapa += 1;
            consultarEtapa();
            link1.classList.remove("active")
            link1.classList.add("bg-white")
        } else {
            alert(situacao.situacao.mensagem)
        }
    })
}

const etapa2 = (form) => {
    const form_conteudo = `
                    <div class="form-floating mb-3">
                        <input type="text" value="${cadUsuario.logradouro}" class="form-control" id="logradouro" name="logradouro" placeholder="Rua do Limoeiro">
                        <label for="logradouro">Logradouro</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input value="${cadUsuario.numero}" class="form-control" id="numero" name="numero" placeholder="12">
                        <label for="numero">Número</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input value="${cadUsuario.complemento}" type="text" class="form-control" id="complemento" name="complemento" placeholder="apto">
                        <label for="complemento">Complemento</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input value="${cadUsuario.bairro}" type="text" class="form-control" id="bairro" name="bairro" placeholder="Bairro">
                        <label for="bairro">Bairro</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input value="${cadUsuario.cidade}" type="text" class="form-control" id="cidade" name="cidade" placeholder="Cidade">
                        <label for="cidade">Cidade</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input value="${cadUsuario.uf}" type="text" class="form-control" id="uf" name="uf" placeholder="UF">
                        <label for="uf">UF</label>
                    </div>
                    <div class="form-floating mb-3">
                        <input value="${cadUsuario.cep}" type="text" class="form-control" id="cep" name="cep" placeholder="CEP">
                        <label for="cep">CEP</label>
                    </div>
                    <div class="text-center">
                        <a href="/usuario/cadastro_usuario/registro2.html">
                            <i class="bi bi-arrow-right fs-1 text-white"></i>
                        </a>
                    </div>
                    <div class="d-flex justify-content-between">
                        <button type="button" id="etapa2-button-prev">Anterior</button>
                        <button type="button" id="etapa2-button-next">Próximo</button>
                    </div>
    `
    form.innerHTML = form_conteudo
    const link2 = document.getElementById("etapa2-link")
    link2.classList.add("active")
    link2.classList.remove("bg-white")
    const btn2_next = document.getElementById("etapa2-button-next")
    const btn2_prev = document.getElementById("etapa2-button-prev")

    addEventFunc(["logradouro", "numero", "complemento", "bairro", "cidade", "uf", "cep"])
    
    const saida = () => {
        link2.classList.remove("active")
        link2.classList.add("bg-white")
        consultarEtapa();
    }
    btn2_next.addEventListener("click", () => {
        let  situacao = cadUsuario.getEtapa2()
        if(situacao.situacao.bool) {
            etapa += 1;
            saida()
        } else {
            alert(situacao.situacao.mensagem)
        }
    })
    btn2_prev.addEventListener("click", () => {
            etapa -= 1;
            saida()
    })
}

const etapa3 = (form) => {
    const form_conteudo = `
        <div class="form-floating mb-3">
            <textarea class="form-control" name="saude_info" id="saude_info" rows="3">${cadUsuario.saude_info}</textarea>
            <label for="saude_info">Nos conte um pouco sobre a sua saúde</label>
        </div>
        <div class="form-floating mb-3">
            <input accept=".pdf" type="file" class="form-control" id="arquivo" name="arquivo" placeholder="PDF">
            <label for="arquivo">Upload do seu histórico médico
            </label>
        </div>
        <div class="text-center">
            <a href="/usuario/cadastro_usuario/registro3.html">
                <i class="bi bi-arrow-right fs-1 text-white"></i>
            </a>
        </div>
        <div class="d-flex justify-content-between">
            <button type="button" id="etapa3-button-prev">Anterior</button>
            <button type="button" id="etapa3-button-next">Próximo</button>
        </div>
`
    form.innerHTML = form_conteudo
    const link3 = document.getElementById("etapa3-link")
    link3.classList.add("active")
    link3.classList.remove("bg-white")
    const btn3_next = document.getElementById("etapa3-button-next")
    const btn3_prev = document.getElementById("etapa3-button-prev")

    addEventFunc(["saude_info", "arquivo"])
    
    const saida = () => {
        link3.classList.remove("active")
        link3.classList.add("bg-white")
        consultarEtapa();
    }
    btn3_next.addEventListener("click", () => {
        let  situacao = cadUsuario.getEtapa3()
        if(situacao.situacao.bool) {
            etapa += 1;
            saida()
        } else {
            alert(situacao.situacao.mensagem)
        }
    })
    btn3_prev.addEventListener("click", () => {
            etapa -= 1;
            saida()
    })
}

const etapa4 = (form) => {
    const form_conteudo = `
         <div class="form-floating mb-3">
            <input value="${cadUsuario.peso}" type="number" class="form-control" id="peso" name="peso">
            <label for="peso">Peso (Kg)</label>
        </div>
        <div class="form-floating mb-3">
            <input value="${cadUsuario.altura}" type="number" class="form-control" id="altura" name="altura">
            <label for="altura">Altura (cm)</label>
        </div>
        <div class="form-floating mb-3">
            <select value="${cadUsuario.tipo_sangue}" class="form-select" id="tipo_sangue" name="tipo_sangue">
                <!-- <option value="">Selecione o seu tipo sanguíneo...</option> -->
                <option value="A">A</option>
                <option value="B">B</option>
                <option value="AB">AB</option>
                <option value="O">O</option>
                <option value="-A">-A</option>
                <option value="-B">-B</option>
                <option value="-AB">-AB</option>
                <option value="-O">-O</option>
            </select>
            <label for="tipo_sangue">Selecione o seu tipo sanguíneo</label>
        </div>
        <div class="text-center">
            <a href="/usuario/cadastro_usuario/concluido.html">
                <i class="bi bi-arrow-right fs-1 text-white"></i>
            </a>
        </div>
        <div class="d-flex justify-content-between">
            <button type="button" id="etapa4-button-prev">Anterior</button>
            <button type="button" id="etapa4-button-next">Próximo</button>
        </div>`
    form.innerHTML = form_conteudo
    const link4 = document.getElementById("etapa4-link")
    link4.classList.add("active")
    link4.classList.remove("bg-white")
    const btn4_next = document.getElementById("etapa4-button-next")
    const btn4_prev = document.getElementById("etapa4-button-prev")

    addEventFunc(["peso", "altura", "tipo_sangue"])
    
    const saida = () => {
        link4.classList.remove("active")
        link4.classList.add("bg-white")
        consultarEtapa();
    }
    btn4_next.addEventListener("click", () => {
        let  situacao = cadUsuario.getEtapa4()
        
        if(situacao.situacao.bool){
            etapa += 1;
            saida()
        } else {
            alert(situacao.situacao.mensagem)
        }
    })
    btn4_prev.addEventListener("click", () => {
            etapa -= 1;
            saida()
    })
}

const etapa5 = (form) => {
    const form_conteudo = `
        <div class="form-floating mb-3">
            <div class="text-center mb-5">
                <h2>Parabéns!</h2>
                <p>Cadastro efetuado com sucesso!</p>
            </div>
            <div class="text-center">
                <p>Clique na seta para voltar para pagina inicial.</p>
            </div>
            
        </div>
        <div class="text-center">
            <a href="/usuario/cadastro_usuario/index.html">
                <i class="bi bi-arrow-right fs-1 text-white"></i>
            </a>
        </div>
        <div class="d-flex justify-content-between">
            <button type="button" id="etapa5-button-prev">Anterior</button>
            <span>
                <button type="button" id="etapa5-button-submit">Finalizar cadastro</button>
            </span>
        </div>
`
    form.innerHTML = form_conteudo
    const link5 = document.getElementById("etapa5-link")
    link5.classList.add("active")
    link5.classList.remove("bg-white")
    const btn5 = document.getElementById("etapa5-button-prev")
    const btn5_submit = document.getElementById("etapa5-button-submit")
    btn5_submit.addEventListener("click", ()=> {
        console.log("lift me up")
        const usuario = cadUsuario.getUsuario()
        cadUsuario.registrarUsuario(usuario)
    })
    btn5.addEventListener("click", () => {
        etapa -= 1;
        consultarEtapa();
        link5.classList.remove("active")
        link5.classList.add("bg-white")
    })
}

const getValue = (e) => {
    const targ = e.target
    const nome = targ.name
    const value = targ.value

    usuario[nome] = value
    cadUsuario[nome] = value
    console.log(cadUsuario)
}

const addEventFunc = (ids) => {
    for (const id of ids){
        let e = document.getElementById(id)
        e.addEventListener("change", (e) => getValue(e))
    }
}