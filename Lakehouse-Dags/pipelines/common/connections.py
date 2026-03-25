import pyiceberg
from s3fs import S3FileSystem
import pyiceberg.catalog.rest

host = "10.0.0.96"

catalog = pyiceberg.catalog.rest.RestCatalog(
    name="catalog_name",
    uri=f"http://{host}:8181/catalog",
    warehouse="lakehouse_warehouse",
)

s3fs = S3FileSystem(
    endpoint_url=f"http://{host}:6000",
    key="ilaybor",
    secret="24342434",
)
