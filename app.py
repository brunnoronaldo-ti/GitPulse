from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World! 🌍"

@app.route("/user/<username>")
def user(username):
    return {
        "username": username,
        "status": "rota funcionando"
    }

if __name__ == "__main__":
    app.run(debug=True)
