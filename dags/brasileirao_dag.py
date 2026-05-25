 from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import sys

sys.path.insert(0, "/opt/airflow/scripts")
from brasileirao_pipeline import (
    coletar_classificacao, coletar_artilheiros,
    coletar_proximos_jogos, coletar_resultados
)

DB_URL = "postgresql://admin:senha123@postgres:5432/brasileirao"

def engine(): return create_engine(DB_URL)

with DAG(
    dag_id="brasileirao_pipeline",
    schedule_interval="0 11 * * *",  # 8h Brasília
    start_date=datetime(2025, 1, 1),
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
) as dag:

    t1 = PythonOperator(task_id="classificacao",  python_callable=lambda: coletar_classificacao(engine()))
    t2 = PythonOperator(task_id="artilheiros",    python_callable=lambda: coletar_artilheiros(engine()))
    t3 = PythonOperator(task_id="proximos_jogos", python_callable=lambda: coletar_proximos_jogos(engine()))
    t4 = PythonOperator(task_id="resultados",     python_callable=lambda: coletar_resultados(engine()))

    [t1, t2, t3] >> t4
