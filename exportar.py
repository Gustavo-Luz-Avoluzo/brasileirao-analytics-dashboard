import pandas as pd
from sqlalchemy import create_engine

load_dotenv()
DB_URL = f"postgresql://postgres:{os.getenv('DB_PASSWORD')}@localhost:5432/brasileirao"
engine = create_engine(DB_URL)

tabelas = ["classificacao", "artilheiros", "jogos"]

for tabela in tabelas:
    df = pd.read_sql(f"SELECT * FROM {tabela}", engine)

    df.to_csv(
        f"{tabela}.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print(f"✓ {tabela}.csv exportado → {len(df)} registros")

print("\nPronto! Arquivos CSV gerados na pasta do projeto.")