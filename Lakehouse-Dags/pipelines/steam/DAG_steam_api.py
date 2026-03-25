from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from cosmos import DbtTaskGroup, ProjectConfig, DbtRunLocalOperator, RenderConfig
from cosmos import ProfileConfig
from cosmos.profiles.trino import TrinoBaseProfileMapping
from pathlib import Path

# from pipelines.common.connections import profile_config, DEFAULT_DBT_ROOT_PATH
from pipelines.common import upsert_iceberg_table
from pipelines.steam.ingestion import load_missing_games
from pipelines.steam.model import SteamGame

DEFAULT_DBT_ROOT_PATH = Path(__file__).parent.parent.parent / "dbt_project"
profile_config = ProfileConfig(
    profile_name="lakehouse_profile",
    target_name="dev",
    profile_mapping=TrinoBaseProfileMapping(
        conn_id="trino",
        profile_args={
            "database": "iceberg",
            "schema": "staging",
            "http_scheme": "http",
        },
    ),
)

with DAG(
    dag_id="get_games_metadata",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["steam-etl"],
) as dag:
    dbt_create_missing_games_table = DbtRunLocalOperator(
        task_id="dbt_create_missing_games_table",
        project_dir=DEFAULT_DBT_ROOT_PATH,
        profile_config=profile_config,
        select=["int_games_to_fetch"],
        install_deps=True,
    )
    
    get_missing_games = PythonOperator(
        task_id="get_missing_games",
        python_callable=load_missing_games,
        op_kwargs={
            "to_read_from_table_identifier": "intermediate.int_games_to_fetch"
            },
    )

    load_to_iceberg = PythonOperator(
        task_id="load_to_iceberg",
        python_callable=upsert_iceberg_table,
        op_kwargs={
            "model": SteamGame,
            "folder_path": "warehouse/raw/steam_data",
            "table_identifier": "staging.steam_data",
            "primary_key": ["steam_appid"]
        },
    )

    dbt_modelling = DbtTaskGroup(
        group_id="dbt_transform",
        project_config=ProjectConfig(DEFAULT_DBT_ROOT_PATH),
        profile_config=profile_config,
        render_config=RenderConfig(select=["stg_steam_api__games_details"]),
        operator_args={"install_deps": True},
    )

    dbt_create_missing_games_table >> get_missing_games >> load_to_iceberg >> dbt_modelling
