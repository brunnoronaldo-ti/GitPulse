//arquivo responsável por trocar o tema da página entre claro e escuro
document.getElementById("trocar-tema").addEventListener("click", function() {
  const body = document.body;
  const button = document.getElementById("trocar-tema");

  //define o tema inicial como claro, caso não tenha nenhum tema definido
  if (!body.classList.contains("tema-claro") && !body.classList.contains("tema-escuro")) {
    body.classList.add("tema-claro");
    button.textContent = "escuro";
    return;
  }

  // Verifica o tema atual e troca para o outro
  if (body.classList.contains("tema-claro")) {
    body.classList.remove("tema-claro");
    body.classList.add("tema-escuro");
    button.textContent = "☀️";
  } else {
    body.classList.remove("tema-escuro");
    body.classList.add("tema-claro");
    button.textContent = "🌙";
  }

  //salva a preferência do usuário no localStorage
  localStorage.setItem("tema", body.classList.contains("tema-claro") ? "claro" : "escuro");
});
