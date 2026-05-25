import os
import requests
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

TOKEN  =  os.getenv("FOOTBALL_DATA_TOKEN")
DB_URL = f"postgresql://postgres:{os.getenv('DB_PASSWORD')}@localhost:5432/brasileirao"

BASE_URL = "https://api.football-data.org/v4"
HEADERS  = {"X-Auth-Token": TOKEN}

def get(endpoint):
    r = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()

def salvar(df, tabela, engine):
    df.to_sql(tabela, engine, if_exists="replace", index=False)

    # salva CSV
    df.to_csv(f"{tabela}.csv", index=False, encoding="utf-8-sig")

    print(f"  ✓ {tabela} → {len(df)} registros")
def coletar_classificacao(engine):
    print("\n[1/3] Coletando classificacao...")
    dados = get("/competitions/BSA/standings")
    tabela = dados["standings"][0]["table"]
    registros = []
    for time in tabela:
        registros.append({
            "posicao":        time["position"],
            "time_nome":      time["team"]["name"],
            "time_sigla":     time["team"]["shortName"],
            "logo_url":       time["team"]["crest"],
            "jogos":          time["playedGames"],
            "vitorias":       time["won"],
            "empates":        time["draw"],
            "derrotas":       time["lost"],
            "gols_pro":       time["goalsFor"],
            "gols_contra":    time["goalsAgainst"],
            "saldo_gols":     time["goalDifference"],
            "pontos":         time["points"],
            "aproveitamento": round(time["points"] / max(time["playedGames"] * 3, 1) * 100, 1),
            "atualizado_em":  datetime.now(),
        })
    salvar(pd.DataFrame(registros), "classificacao", engine)

def coletar_artilheiros(engine):
    print("\n[2/3] Coletando artilheiros...")
    dados = get("/competitions/BSA/scorers?limit=20")
    registros = []
    for i, s in enumerate(dados["scorers"], start=1):
        registros.append({
            "posicao":       i,
            "jogador_nome":  s["player"]["name"],
            "time_nome":     s["team"]["name"],
            "time_sigla":    s["team"]["shortName"],
            "gols":          s.get("goals", 0),
            "assistencias":  s.get("assists", 0) or 0,
            "jogos":         s.get("playedMatches", 0),
            "atualizado_em": datetime.now(),
        })
    salvar(pd.DataFrame(registros), "artilheiros", engine)

def coletar_jogos(engine):
    print("\n[3/3] Coletando jogos...")
    dados = get("/competitions/BSA/matches?limit=100")
    registros = []
    for j in dados["matches"]:
        score = j["score"]["fullTime"]
        registros.append({
            "jogo_id":       j["id"],
            "rodada":        j["matchday"],
            "data":          j["utcDate"][:10],
            "status":        j["status"],
            "time_casa":     j["homeTeam"]["name"],
            "time_casa_sigla": j["homeTeam"]["shortName"],
            "gols_casa":     score["home"],
            "gols_fora":     score["away"],
            "time_fora":     j["awayTeam"]["name"],
            "time_fora_sigla": j["awayTeam"]["shortName"],
            "atualizado_em": datetime.now(),
        })
    salvar(pd.DataFrame(registros), "jogos", engine)

def executar_pipeline():
    print("=" * 45)
    print("  Brasileirao Analytics - football-data.org")
    print(f"  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 45)
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✓ PostgreSQL conectado")
    coletar_classificacao(engine)
    coletar_artilheiros(engine)
    coletar_jogos(engine)
    print("\n✓ Pipeline concluido!")

if __name__ == "__main__":
    executar_pipeline()