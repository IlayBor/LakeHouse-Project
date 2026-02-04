from pathlib import Path

from cosmos import DbtDag, ProjectConfig, ProfileConfig, RenderConfig
from cosmos.profiles import TrinoLDAPProfileMapping
from datetime import datetime

# DEFAULT_DBT_ROOT_PATH = str(Path(__file__).parent/"dbt_project")

profile_config = ProfileConfig(
    profile_name="lakehouse_profile",
    target_name="dev",
    profile_mapping=TrinoLDAPProfileMapping(
        conn_id="trino",
        profile_args={
            "database": "iceberg",
            "schema": "silver",
            "http_scheme": "http",
        },
    ),
)

basic_cosmos_dag = DbtDag(
    project_config=ProjectConfig("/opt/airflow/dags/dbt_project"),
    profile_config=profile_config,
    render_config=RenderConfig(
        select=["game_list"]
    ),

    operator_args={"install_deps": True},
    schedule="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    dag_id="example",
    default_args={"retries": 0},
)