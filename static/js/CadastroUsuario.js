import {calcularIdade, validarCPF, validarEmail, compararSenhas, senhasVazias} from "/static/utils.js"

export default class CadastroUsuario{
    constructor() {
        this.nome_completo = "";
        this.cpf = "";
        this.data_nascimento = "";
        this.telefone = "";
        this.telefone_emergencia = "";
        this.email = "";
        this.senha = "";
        this.conf_senha = ""
        this.logradouro = ""
        this.numero = ""
        this.complemento = ""
        this.bairro = ""
        this.cidade = ""
        this.uf = ""
        this.cep = ""
        this.saude_info = ""
        this.arquivo = ""
        this.peso = 0.0;
        this.altura = 0.0;
        this.tipo_sangue = ""
    }

    getEtapa1(){
        let etapa1 = {
            "props": {
                "nome_completo": this.nome_completo,
                "cpf": this.cpf,
                "data_nascimento": this.data_nascimento,
                "telefone": this.telefone,
                "telefone_emergencia": this.telefone_emergencia,
                "email": this.email,
                "senha": this.senha,
                "conf_senha": this.conf_senha
            },
            "situacao": this.verificarCampos(1)
        }
        return etapa1
    }

    getEtapa2(){
        let etapa2 = {
            "props": {
                "logradouro": this.logradouro,
                "numero": this.numero,
                "complemento": this.complemento,
                "bairro": this.bairro,
                "cidade": this.cidade,
                "uf": this.uf,
                "cep": this.cep,
            },
            "situacao": this.verificarCampos(2)
        }
        return etapa2
    }
    
    getEtapa3(){
        let etapa2 = {
            "props": {
                "saude_info": this.saude_info,
                "arquivo": this.arquivo,
            },
            "situacao": this.verificarCampos(3)
        }
        return etapa2
    }

    getEtapa4(){
        let etapa3 = {
            "props": {
                "peso": this.peso,
                "altura": this.altura,
                "tipo_sangue": this.tipo_sangue,
            },
            "situacao": this.verificarCampos(4)
        }
        return etapa3
    }

    verificarCampos(etapa){
        if(etapa === 1){
            if(this.nome_completo.length < 3){
                return {
                    "status": "inválido",
                    "mensagem": "Tamanho do nome inválido",
                    "bool": false
                }
            }
            if(!validarCPF(this.cpf)){
                return {
                    "status": "inválido",
                    "mensagem": "Tamanho do cpf inválido",
                    "bool": false
                }
            }
            if(!calcularIdade(this.data_nascimento)){
                return {
                    "status": "inválido",
                    "mensagem": "O doador precisa ter ni mínimo 16 anos",
                    "bool": false
                }
            }
            if(!validarEmail(this.email)){
                return {
                    "status": "inválido",
                    "mensagem": "Email inválido",
                    "bool": false
                }
            }
            if(!senhasVazias(this.senha, this.conf_senha)){
                return {
                    "status": "inválido",
                    "mensagem": "As senhas não podem estar vaziar",
                    "bool": false
                }
            }
            if(!compararSenhas(this.senha, this.conf_senha)){
                return {
                    "status": "inválido",
                    "mensagem": "As senhas não são iguais",
                    "bool": false
                }
            }
            return {
                "status": "válido",
                "mensagem": "ok",
                "bool": true
            }
        } 
        
        else if(etapa === 2){
            if(!this.logradouro.length){
                return {
                    "status": "inválido",
                    "mensagem": "Nos informe o seu logradouro",
                    "bool": false
                }
            }
            if(!this.numero){
                return {
                    "status": "inválido",
                    "mensagem": "Nos infome o seu número",
                    "bool": false
                }
            }
            if(!this.complemento){
                return {
                    "status": "inválido",
                    "mensagem": "Nos infome um complemento",
                    "bool": false
                }
            }
            if(!this.bairro){
                return {
                    "status": "inválido",
                    "mensagem": "Nos infome o seu bairro",
                    "bool": false
                }
            }
            if(!this.cidade){
                return {
                    "status": "inválido",
                    "mensagem": "Nos infome a sua cidade",
                    "bool": false
                }
            }
            if(!this.uf){
                return {
                    "status": "inválido",
                    "mensagem": "Nos infome o seu Estado",
                    "bool": false
                }
            }
            if(!this.cep){
                return {
                    "status": "inválido",
                    "mensagem": "Nos infome o seu CEP",
                    "bool": false
                }
            }
            return {
                "status": "válido",
                "mensagem": "ok",
                "bool": true
            }
            
        }
        
        else if(etapa === 3){
            if(!this.saude_info.length){
                return {
                    "status": "inválido",
                    "mensagem": "Nos informe a sua saúde",
                    "bool": false
                }
            }
            if(!this.arquivo){
                return {
                    "status": "inválido",
                    "mensagem": "Faça o upload de um atestado médico em pdf",
                    "bool": false
                }
            }
            return {
                "status": "válido",
                "mensagem": "ok",
                "bool": true
            }
            
        }
        else if(etapa === 4){
            if(this.peso < 50.0){
                return {
                    "status": "inválido",
                    "mensagem": "O peso não pode ser inferior a 50.0Kg",
                    "bool": false
                }
            }
            if(this.altura < 1.50){
                return {
                    "status": "inválido",
                    "mensagem": "A altura não pode ser inferior a 1,50m",
                    "bool": false
                }
            }
            if(!this.tipo_sangue) {
                return {
                    "status": "inválido",
                    "mensagem": "Escolha um tipo de sangue válido",
                    "bool": false
                }
            }
            return {
                "status": "válido",
                "mensagem": "ok",
                "bool": true
            }
            
        }
        
    }

    getUsuario(){
        return {
            id: 0,
            nome_completo: this.nome_completo,
            email: this.email,
            senha: this.senha,
            telefone: this.telefone,
            telefone_emergencia: this.telefone_emergencia,
            cpf: this.cpf,
            data_nascimento: this.data_nascimento,
            logradouro: this.logradouro,
            numero: this.numero,
            complemento: this.complemento,
            bairro: this.bairro,
            cidade: this.cidade,
            uf: this.uf,
            cep: this.cep,
            informacao_saude: this.saude_info,
            arquivo_exame: "arquivo-exame.pdf",
            peso: this.peso,
            altura: this.altura,
            tipo_sangue: this.tipo_sangue,
        }
    }

    async registrarUsuario(usuario){
        const res = await axios({
            method: "POST",
            url: "/cadastro",
            data: usuario
        })

        console.log(res, "resposte")
    }
}
