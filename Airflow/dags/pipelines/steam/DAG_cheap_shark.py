from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from cosmos import DbtTaskGroup, ProjectConfig, RenderConfig

from pipelines.common.connections import profile_config, DEFAULT_DBT_ROOT_PATH
from pipelines.common.transform import upsert_iceberg_table
from pipelines.steam.ingestion import load_game_data
from pipelines.steam.model import SteamGame

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
            "to_read_from_table_identifier": "bronze.cheapshark_data"
            },
    )

    load_to_iceberg = PythonOperator(
        task_id="load_to_iceberg",
        python_callable=upsert_iceberg_table,
        op_kwargs={
            "model": SteamGame,
            "folder_path": "warehouse/raw/steam_data",
            "table_identifier": "bronze.steam_data",
            "primary_key": ["steam_appid"]
        },
    )

    # dbt_modelling = DbtTaskGroup(
    #     group_id="dbt_transform",
    #     project_config=ProjectConfig(DEFAULT_DBT_ROOT_PATH),
    #     profile_config=profile_config,
    #     render_config=RenderConfig(select=["+fct_deals"]),
    #     operator_args={"install_deps": True},
    # )

    load_json >> load_to_iceberg # >> dbt_modelling
