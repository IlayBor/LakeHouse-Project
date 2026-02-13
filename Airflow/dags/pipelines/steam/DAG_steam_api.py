from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from cosmos import DbtTaskGroup, ProjectConfig, RenderConfig
from cosmos import ProfileConfig
from cosmos.profiles.trino import TrinoBaseProfileMapping
from pathlib import Path

# from pipelines.common.connections import profile_config, DEFAULT_DBT_ROOT_PATH
from pipelines.common.transform import upsert_iceberg_table
from pipelines.steam.ingestion import load_game_data
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
    dag_id="steam_data_ingestion",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["steam-etl"],
) as dag:
    load_json = PythonOperator(
        task_id="load_game_data",
        python_callable=load_game_data,
        op_kwargs={
            "to_read_from_table_identifier": "staging.cheapshark_data"
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
        render_config=RenderConfig(select=["+stg_steam_api__game_details"]),
        operator_args={"install_deps": True},
    )

    load_json >> load_to_iceberg >> dbt_modelling
