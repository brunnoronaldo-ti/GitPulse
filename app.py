from reportlab.lib.pagesizes import A4 # Importa o tamanho A4 para o PDF
from reportlab.pdfgen import canvas # Importa a classe canvas para criar o PDF
from reportlab.lib.units import cm # Importa a unidade centímetro para posicionamento no PDF
import io # Importa o módulo io para manipulação de streams de dados
from flask import Flask, render_template, request, send_file # Importa o Flask e funções relacionadas para criar a aplicação web
import requests # Importa o módulo requests para fazer requisições HTTP
import matplotlib.pyplot as plt # Importa o matplotlib para gerar gráficos
import tempfile # Importa o módulo tempfile para criar arquivos temporários
import os # Importa o módulo os para manipulação de arquivos


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

#busca as linguagens usadas em um repositório específico
def get_repo_languages(owner, repo_name):
    url = f"https://api.github.com/repos/{owner}/{repo_name}/languages"
    response = requests.get(url)

    if response.status_code != 200:
        return {}

    return response.json()

#soma a quantidade de bytes por linguagem em todos os repositórios do usuário
def sum_languages_by_bytes(username, repos):
    total_languages = {}

    for repo in repos:
        repo_name = repo["name"]
        languages = get_repo_languages(username, repo_name)

        for lang, bytes_count in languages.items():
            total_languages[lang] = total_languages.get(lang, 0) + bytes_count

    return total_languages

#calcula a porcentagem de uso de cada linguagem
def calculate_language_percentages(languages_by_bytes):
    total_bytes = sum(languages_by_bytes.values())
    percentages = {}

    for lang, bytes_count in languages_by_bytes.items():
        percent = (bytes_count / total_bytes) * 100
        percentages[lang] = round(percent, 2)

    return percentages

#ordena as linguagens pela quantidade de bytes em ordem decrescente
def sort_languages(data):
    return dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

#gera um gráfico de pizza das linguagens usadas
def generate_language_chart(language_percentages):
    languages = list(language_percentages.keys())
    values = list(language_percentages.values())

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp_path = temp_file.name
    temp_file.close()

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=languages, autopct="%1.1f%%", startangle=140)
    plt.title("Distribuição de Linguagens")
    plt.tight_layout()
    plt.savefig(temp_path)
    plt.close()

    return temp_path

#gera um relatório em PDF com os dados do usuário
def generate_pdf(username, language_percentages):
    chart_path = generate_language_chart(language_percentages)
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 2 * cm

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(2 * cm, y, "GitPulse — Relatório de Linguagens")

    pdf.drawImage(
    chart_path,
    2 * cm,
    y - 10 * cm,
    width=12 * cm,
    height=12 * cm,
    preserveAspectRatio=True
    )

    y -= 12 * cm

    y -= 1.5 * cm
    pdf.setFont("Helvetica", 12)
    pdf.drawString(2 * cm, y, f"Usuário: {username}")

    y -= 1 * cm
    pdf.drawString(2 * cm, y, "Distribuição de linguagens:")

    y -= 1 * cm

    pdf.setFont("Helvetica", 11)
    for lang, percent in language_percentages.items():
        pdf.drawString(3 * cm, y, f"{lang}: {percent}%")
        y -= 0.7 * cm

        if y < 2 * cm:
            pdf.showPage()
            y = height - 2 * cm
            pdf.setFont("Helvetica", 11)

    pdf.showPage()
    pdf.save()
    os.remove(chart_path) # Remove o arquivo temporário do gráfico

    buffer.seek(0)
    return buffer

#--------------------------------------------------------
#ROTAS:

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
    languages_by_bytes = sum_languages_by_bytes(username, repos)
    language_percentages = calculate_language_percentages(languages_by_bytes)
    language_percentages = sort_languages(language_percentages)


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


if __name__ == "__main__":
    app.run(debug=True)
