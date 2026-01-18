from flask import Flask, render_template, request 
import requests

app = Flask(__name__)
GITHUB_API_URL = "https://api.github.com/users" # URL base da API do GitHub (necessária para buscar dados dos usuários)

#busca dados gerais do usuário
def get_user_data(username):
    url = f"{GITHUB_API_URL}/{username}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    return response.json() 

#busca os repositórios do usuário
def get_user_repos(username):
    url = f"{GITHUB_API_URL}/{username}/repos"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    return response.json()

#conta a quantidade de repositórios por linguagem
def count_languages(repos):
    languages = {}

    for repo in repos:
        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1

    return languages

@app.route("/")
def home():
    return render_template("index.html")
        
@app.route("/user", methods=["POST"])
def user():
    username = request.form.get("username")

    if not username:
        return render_template("result.html", error="Username não informado")

    user_data = get_user_data(username)
    repos = get_user_repos(username)
    languages = count_languages(repos)


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
        languages=languages
    )

if __name__ == "__main__":
    app.run(debug=True)
