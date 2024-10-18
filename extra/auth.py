from github import Github, Auth

def validate_github_token(token):
    auth = Auth.Token(token)
    g = Github(auth=auth)
    repos = g.get_user().get_repos()

    if repos.totalCount == 0:
        raise ValueError("No tienes repositorios asociados con este token.")

    return token  # Retorna el token si es válido
