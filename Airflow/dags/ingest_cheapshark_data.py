import os
from pathlib import Path
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# 1. Define the path using the robust environment variable method
# This defaults to /opt/airflow if not set, which is standard for Docker
DEFAULT_DBT_ROOT_PATH = str(Path(__file__).parent/"dbt_project")
STR = "/opt/airflow/dags/dbt_project"

def print_path_value():
    print(f"--- DEBUG OUTPUT ---")
    print(f"DEFAULT_DBT_ROOT_PATH: {DEFAULT_DBT_ROOT_PATH}")
    print(f"STR: {STR}")
    print(f"--------------------")

with DAG(
    dag_id="debug_dbt_path",
    schedule=None, # Trigger manually
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["debug"],
) as dag:

    print_task = PythonOperator(
        task_id="print_the_path",
        python_callable=print_path_value
    )