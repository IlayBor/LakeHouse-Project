import os
from pathlib import Path
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, RenderConfig
from cosmos.profiles.trino import TrinoBaseProfileMapping

from cheap_shark.ingestion import load_cheapshark_pages
from cheap_shark.transformation import transform_to_iceberg2

DEFAULT_DBT_ROOT_PATH = Path(__file__).parent.parent / "dbt_project"

profile_config = ProfileConfig(
    profile_name="lakehouse_profile",
    target_name="dev",
    profile_mapping=TrinoBaseProfileMapping(
        conn_id="trino",
        profile_args={
            "database": "iceberg",
            "schema": "gold",
            "http_scheme": "http",
        },
    ),
)


with DAG(
    dag_id="cheap_shark_ingestion",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["steam-etl"],
) as dag:
    load_json = PythonOperator(
        task_id="load_json_deals",
        python_callable=load_cheapshark_pages,
        op_kwargs={"start_page": 0, "end_page": 5},
    )

    convert_to_iceberg = PythonOperator(
        task_id="convert_to_iceberg",
        python_callable=transform_to_iceberg2,
        op_kwargs={
            "source_file": "warehouse/raw/cheapshark_data",
            "target_table": "bronze.cheapshark_data",
        },
    )

    dbt_modelling = DbtTaskGroup(
        group_id="dbt_transform",
        project_config=ProjectConfig(DEFAULT_DBT_ROOT_PATH),
        profile_config=profile_config,
        render_config=RenderConfig(select=["+fct_deals"]),
        operator_args={"install_deps": True},
    )

    load_json >> convert_to_iceberg >> dbt_modelling
