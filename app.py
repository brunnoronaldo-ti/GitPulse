from flask import Flask, render_template, request, send_file # Importa o Flask e funções relacionadas para criar a aplicação web
from pdf import generate_pdf # Importa a função generate_pdf do módulo pdf para gerar PDFs
from github_search import get_user_data, get_user_repos # Importa funções do módulo github_search para buscar dados do GitHub
from accounts import (
    count_languages, 
    sum_languages_by_bytes,
    calculate_language_percentages,
    sort_languages
)# Importa várias funções do módulo accounts para processar dados dos repositórios

app = Flask(__name__)

#--------------------------------------------------------
#ROTAS:

@app.route("/")
def home():
    return render_template("index.html")
        
@app.route("/user", methods=["POST"])
def user():
    username = request.form.get("username")

    print("USERNAME:", username)

    if not username:
        return render_template("result.html", error="Username não informado")

    user_data = get_user_data(username)
    repos = get_user_repos(username)

    print("REPOS:", len(repos))

    languages = count_languages(repos)
    languages_by_bytes = sum_languages_by_bytes(username, repos)
    language_percentages = calculate_language_percentages(languages_by_bytes)
    language_percentages = sort_languages(language_percentages)

    print("LANGUAGES:", languages)
    print("BYTES:", languages_by_bytes)

    if not user_data:
        return render_template(
            "result.html",
            error="Usuário não encontrado"
        )

    return render_template(
        "result.html",
        username=user_data["login"],
        public_repos=user_data["public_repos"],
        followers=user_data["followers"],
        repos=repos,
        languages=languages,
        languages_by_bytes=languages_by_bytes,
        language_percentages=language_percentages
    )

@app.route("/download/pdf/<username>")
def download_pdf(username):
    repos = get_user_repos(username)
    languages_by_bytes = sum_languages_by_bytes(username, repos)
    language_percentages = calculate_language_percentages(languages_by_bytes)
    language_percentages = sort_languages(language_percentages)

    if not language_percentages:
        return "Erro ao gerar PDF", 400

    pdf_buffer = generate_pdf(username, language_percentages)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"GitPulse_{username}.pdf",
        mimetype="application/pdf"
    )
#--------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
