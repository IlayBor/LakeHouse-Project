from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from cosmos.operators.local import DbtCloneLocalOperator
from cosmos import ProfileConfig, ProjectConfig
from pathlib import Path

DBT_PROJ_DIR = str(Path(__file__).parent / "dbt_project")

profile_config = ProfileConfig(
    profile_name="lakehouse_profile",
    target_name="dev",
)

# Python function to execute
def print_hello_python():
    print("Hello from the Python Operator!")

# DAG Definition
with DAG(
    dag_id="hello_world_test",
    start_date=datetime(2024, 1, 1),
    schedule=None, # Trigger manually
    catchup=False,
    tags=["test", "debug"]
) as dag:

    clone_operator = DbtCloneLocalOperator(
        profile_config=profile_config,
        project_dir=DBT_PROJ_DIR,
        task_id="debug",
        dbt_cmd_flags=["debug"],
        install_deps=True,
        append_env=True,
    )