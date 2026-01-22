//arquivo responsável por trocar o tema da página entre claro e escuro

document.getElementById("trocar-tema").addEventListener("click", function() {
  const body = document.body;
  const button = document.getElementById("trocar-tema");

  if (body.classList.contains("light-theme")) {
    body.classList.remove("light-theme");
    body.classList.add("dark-theme");
    button.textContent = "claro";
  } else {
    body.classList.remove("dark-theme");
    body.classList.add("light-theme");
    button.textContent = "escuro";
  }

  //salva a preferência do usuário no localStorage
  localStorage.setItem("tema", body.classList.contains("tema-claro") ? "claro" : "escuro");
});
