const form = document.getElementById("form");
const nome = document.getElementById("nome");
const email = document.getElementById("email");
const senha = document.getElementById("password");
const cpf = document.getElementById("cpf");
const endereco = document.getElementById("endereco");
const estado = document.getElementById("estado");
const cidade = document.getElementById("cidade");

const msg = document.getElementById("msg");
const regras = document.getElementById("regras");

function showMessage(texto, ok) {
  msg.style.display = "block";
  msg.className = "msg " + (ok ? "ok" : "erro");
  msg.textContent = texto;
}

function validarEmail(v) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim());
}

function validarCPF(v) {
  const s = v.replace(/\D/g, "");
  if (s.length !== 11 || /^(\d)\1+$/.test(s)) return false;

  let soma = 0, resto;

  for (let i = 1; i <= 9; i++) {
    soma += parseInt(s.substring(i - 1, i)) * (11 - i);
  }

  resto = (soma * 10) % 11;
  if (resto === 10 || resto === 11) resto = 0;
  if (resto !== parseInt(s.substring(9, 10))) return false;

  soma = 0;
  for (let i = 1; i <= 10; i++) {
    soma += parseInt(s.substring(i - 1, i)) * (12 - i);
  }

  resto = (soma * 10) % 11;
  if (resto === 10 || resto === 11) resto = 0;
  if (resto !== parseInt(s.substring(10, 11))) return false;

  return true;
}

function validarSenha(v) {
  const s = v.trim();
  const erros = [];

  if (s.length < 8) erros.push("Senha deve ter no mínimo 8 caracteres.");
  if (!/[A-Za-z]/.test(s)) erros.push("Senha deve ter pelo menos 1 letra.");
  if (!/\d/.test(s)) erros.push("Senha deve ter pelo menos 1 número.");

  return erros;
}

form.addEventListener("submit", (e) => {
  msg.style.display = "none";
  regras.innerHTML = "";

  const erros = [];

  if (nome.value.trim().length < 3) {
    erros.push("Nome deve ter pelo menos 3 caracteres.");
  }

  if (!validarEmail(email.value)) {
    erros.push("E-mail inválido.");
  }

  if (!validarCPF(cpf.value)) {
    erros.push("CPF inválido.");
  }

  erros.push(...validarSenha(senha.value));

  if (endereco.value.trim().length < 5) {
    erros.push("Endereço muito curto.");
  }

  if (estado.value === "") {
    erros.push("Selecione um estado.");
  }

  if (cidade.value.trim().length < 2) {
    erros.push("Cidade inválida.");
  }

  if (erros.length > 0) {
    e.preventDefault();
    regras.innerHTML = erros.map(er => `<li>${er}</li>`).join("");
    showMessage("Corrija os itens acima antes de enviar.", false);
  } else {
    showMessage("Enviando dados...", true);
  }
});