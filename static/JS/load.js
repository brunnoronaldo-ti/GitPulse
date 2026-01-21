//arquivo que invalida o clique no botão caso o campo esteja vazio
function mostrarloading(event) {
    const usernameInput = document.querySelector('input[name="username"]');
    if (!usernameInput.value.trim()) {
        event.preventDefault();
        return;
    }

    const loadingDiv = document.getElementById("loading");
    if (loadingDiv) {
        loadingDiv.showPopover();
    }
}
