import pyiceberg
from s3fs import S3FileSystem
import pyiceberg.catalog.rest
# from cosmos import ProfileConfig
# from cosmos.profiles.trino import TrinoBaseProfileMapping
# from pathlib import Path

host = "10.0.0.97"

catalog = pyiceberg.catalog.rest.RestCatalog(
    name="catalog_name",
    uri=f"http://{host}:8181/catalog",
    warehouse="lakehouse_warehouse",
)

s3fs = S3FileSystem(
    endpoint_url=f"http://{host}:9000",
    key="ilaybor",
    secret="24342434",
)

# DEFAULT_DBT_ROOT_PATH = Path(__file__).parent.parent.parent / "dbt_project"
# profile_config = ProfileConfig(
#     profile_name="lakehouse_profile",
#     target_name="dev",
#     profile_mapping=TrinoBaseProfileMapping(
#         conn_id="trino",
#         profile_args={
#             "database": "iceberg",
#             "schema": "staging",
#             "http_scheme": "http",
#         },
#     ),
# )

