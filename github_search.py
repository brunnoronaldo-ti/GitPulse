import requests # Importa o módulo requests para fazer requisições HTTP

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
