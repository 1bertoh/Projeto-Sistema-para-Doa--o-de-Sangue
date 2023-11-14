export const calcularIdade = (dataNascimento) => {
  const dataAtual = new Date();
  const dataNasc = new Date(dataNascimento);

  let idade = dataAtual.getFullYear() - dataNasc.getFullYear();

  const mesAtual = dataAtual.getMonth();
  const diaAtual = dataAtual.getDate();
  const mesNasc = dataNasc.getMonth();
  const diaNasc = dataNasc.getDate();

  if (mesAtual < mesNasc || (mesAtual === mesNasc && diaAtual < diaNasc)) {
    idade--;
  }

  return idade >= 16;
}

export const validarCPF =  (cpf) => {
  // Remove todos os caracteres não numéricos
      cpf = cpf.replace(/\D/g, '');
    
      // Verifica se o CPF tem 11 dígitos
      if (cpf.length !== 11) {
        return false;
      }
    
      // Verifica se o CPF possui apenas dígitos repetidos
      if (/^(\d)\1{10}$/.test(cpf)) {
        return false;
      }
    
      // Retorna true se todas as validações passarem
      return true;
}

export const validarEmail = (email) => {
  // Expressão regular para validar o formato do email
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  // Retorna true se o email passar na validação
  return regex.test(email);
}

export const compararSenhas = (senha1, senha2) => {
    return senha1 === senha2
}

export const senhasVazias = (senha1, senha2) => {
    if(!senha1 || !senha2){
        return false
    }
    return true
}

//IR FORMATANDO AS ENTRADAS NOS CAMPOS DE PESO E ALTURA
export const formatarParaFloat = (entrada) => {
  const inputValue = entrada;
  
  // Remove caracteres não numéricos, exceto ponto (.) e vírgula (,)
  const cleanedValue = inputValue.replace(/[^0-9.,]/g, '');

  // Substitui vírgula (,) por ponto (.)
  const floatValue = parseFloat(cleanedValue.replace(',', '.'));

  // Verifica se o valor é um número válido antes de atribuí-lo ao campo
  if (!isNaN(floatValue)) {
    input.value = floatValue.toFixed(2); // Define o valor formatado com 2 casas decimais
  } else {
    input.value = ''; // Limpa o campo se o valor não for válido
  }
}