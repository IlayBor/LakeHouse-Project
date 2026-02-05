import os
from pathlib import Path
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, RenderConfig
from cosmos.profiles.trino import TrinoBaseProfileMapping

from steam.ingestion import load_json_deals_data
from steam.transformation import transform_to_iceberg

DEFAULT_DBT_ROOT_PATH = Path(__file__).parent/"dbt_project"

profile_config = ProfileConfig(
    profile_name="lakehouse_profile",
    target_name="dev",
    profile_mapping=TrinoBaseProfileMapping(
        conn_id="trino",
        profile_args={
            "database": "iceberg",
            "schema": "silver",
            "http_scheme": "http",
        },
    ),
)


with DAG(
    dag_id="steam_ingestion",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,  
    tags=["steam-etl"],
) as dag:

    load_json = PythonOperator(
        task_id="load_json",
        python_callable=load_json_deals_data
    ),

    convert_to_iceberg = PythonOperator(
        task_id="convert_to_iceberg",
        python_callable=transform_to_iceberg
    )

    dbt_modelling = DbtTaskGroup(
        group_id="dbt_transform",
        project_config=ProjectConfig(DEFAULT_DBT_ROOT_PATH),
        profile_config=profile_config,
        render_config=RenderConfig(
            select=["+game_list"]
        ),
        operator_args={"install_deps": True},
    )

    load_json >> convert_to_iceberg >> dbt_modelling

