const modal = document.getElementById('login-modal');

modal.close();

// Abre o dialog como Modal
function openLogin() {
    modal.showModal();
}

// Fecha o dialog
function closeLogin() {
    modal.close();
}

// Fecha se clicar fora da caixa (no fundo escuro)
modal.addEventListener('click', (e) => {
    const dialogDimensions = modal.getBoundingClientRect();
    if (
        e.clientX < dialogDimensions.left ||
        e.clientX > dialogDimensions.right ||
        e.clientY < dialogDimensions.top ||
        e.clientY > dialogDimensions.bottom
    ) {
        modal.close();
    }
});

// Função para mostrar o login
function showLogin(event) {
    event.preventDefault();
    openLogin();
}

// Função para esconder o login
function hideLogin(event) {
    event.preventDefault();
    closeLogin();
}

// Validação do formulário de login
const form = modal.querySelector('form');
form.addEventListener('submit', (e) => {
    if (!form.checkValidity()) {
        e.preventDefault();
        alert("Por favor, preencha todos os campos corretamente.");
    }
});

// Alterar o botão ao enviar o formulário
form.onsubmit = () => {
    const btn = form.querySelector('input[type="submit"]');
    btn.value = "Entrando...";
    btn.disabled = true;
};
