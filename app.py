from flask import Flask, render_template, request # Framework web leve para Python 
import requests

app = Flask(__name__)
GITHUB_API_URL = "https://api.github.com/users" # URL base da API do GitHub (necessária para buscar dados dos usuários)

def get_user_data(username):
    url = f"{GITHUB_API_URL}/{username}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    return response.json() 
    
@app.route("/")
def home():
    return render_template("index.html")
        
@app.route("/user", methods=["POST"])
def user():
    username = request.form.get("username")

    if not username:
        return {"error": "Username não informado"}, 400

    data = get_user_data(username)

    if not data:
        return {"error": "Usuário não encontrado"}, 404

    return {
        "username": data["login"],
        "public_repos": data["public_repos"],
        "followers": data["followers"]
    }


if __name__ == "__main__":
    app.run(debug=True)
