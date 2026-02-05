import os
from pathlib import Path
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


DEFAULT_DBT_ROOT_PATH = str(Path(__file__).parent/"dbt_project")
STR = "/opt/airflow/dags/dbt_project"

def print_path_value():
    print(f"--- DEBUG OUTPUT ---")
    print(f"DEFAULT_DBT_ROOT_PATH: {DEFAULT_DBT_ROOT_PATH}, {type(DEFAULT_DBT_ROOT_PATH)}")
    print(f"STR: {STR}, {type(STR)}")
    print(f"--------------------")

with DAG(
    dag_id="debug_dbt_path",
    schedule=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["debug"],
) as dag:

    print_task = PythonOperator(
        task_id="print_the_path",
        python_callable=print_path_value
    )