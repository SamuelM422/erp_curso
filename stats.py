import requests
from collections import defaultdict
from datetime import datetime, timedelta
from datetime import UTC
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# ===============================
# CONFIGURAÇÕES
# ===============================
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = "SamuelM422"
REPO = 'erp_curso'
#REPO = "curso-django-projeto1"

today = datetime.now(UTC)
since_date = today - timedelta(days=0)
SINCE = since_date.strftime("%Y-%m-%dT00:00:00Z")
UNTIL = today.strftime("%Y-%m-%dT23:59:59Z")

# ===============================
# SETUP
# ===============================
BASE_URL = f"https://api.github.com/repos/{OWNER}/{REPO}"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_commits():
    commits = []
    page = 1
    while True:
        params = {"since": SINCE, "until": UNTIL, "page": page, "per_page": 100}
        r = requests.get(f"{BASE_URL}/commits", headers=HEADERS, params=params)
        r.raise_for_status()
        data = r.json()
        if not data:
            break
        commits.extend(data)
        page += 1
    return commits

def get_commit_stats(commits):
    stats = defaultdict(lambda: {"commits": 0, "additions": 0, "deletions": 0})
    for commit in commits:
        author_name = commit["commit"]["author"]["name"]
        sha = commit["sha"]

        # Pega detalhes do commit (para additions/deletions)
        r = requests.get(f"{BASE_URL}/commits/{sha}", headers=HEADERS)
        r.raise_for_status()
        commit_data = r.json()

        stats[author_name]["commits"] += 1
        for f in commit_data.get("files", []):
            stats[author_name]["additions"] += f["additions"]
            stats[author_name]["deletions"] += f["deletions"]
    return stats

def main():
    print("📡 Buscando commits...")
    commits = get_commits()
    print(f"✅ {len(commits)} commits encontrados.")

    if not commits:
        print("⚠️ Nenhum commit encontrado no período informado.")
        return

    print("📊 Calculando estatísticas...")
    stats = get_commit_stats(commits)

    if not stats:
        print("⚠️ Nenhum dado de estatística gerado.")
        return

    # Converte para DataFrame
    df = pd.DataFrame([
        {"Autor": author, **data} for author, data in stats.items()
    ])
    df = df.sort_values(by="commits", ascending=False)

    print("\n=== Estatísticas por Autor ===")
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()
