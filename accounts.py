import requests # Importa o módulo requests para fazer requisições HTTP
from github_search import get_user_data, get_user_repos # Importa funções do módulo github_search para buscar dados do GitHub   

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
