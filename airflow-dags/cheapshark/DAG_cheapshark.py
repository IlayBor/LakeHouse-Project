from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from cosmos import DbtTaskGroup, ProjectConfig, RenderConfig
from cosmos import ProfileConfig
from cosmos.profiles.trino import TrinoBaseProfileMapping
from pathlib import Path

from pipelines.common import upsert_iceberg_table
from pipelines.cheapshark.ingestion import load_cheapshark_pages
from pipelines.cheapshark.model import GameDeal
 
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
    dag_id="get_cheapshark_deals",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["steam-etl"],
) as dag:
    load_json = PythonOperator(
        task_id="load_json_deals",
        python_callable=load_cheapshark_pages,
        op_kwargs={
            "start_page": 0,
            # "end_page": 5
        },
    )

    load_to_iceberg = PythonOperator(
        task_id="load_to_iceberg",
        python_callable=upsert_iceberg_table,
        op_kwargs={
            "model": GameDeal,
            "folder_path": "warehouse/raw/cheapshark_data",
            "table_identifier": "staging.cheapshark_data",
            "primary_key": ["dealID", "ingestionDate"],
        },
    )

    dbt_modelling = DbtTaskGroup(
        group_id="dbt_transform",
        project_config=ProjectConfig(DEFAULT_DBT_ROOT_PATH),
        profile_config=profile_config,
        render_config=RenderConfig(select=["+stg_cheapshark_api__game_deals"]),
        operator_args={"install_deps": True},
    )

    load_json >> load_to_iceberg >> dbt_modelling
