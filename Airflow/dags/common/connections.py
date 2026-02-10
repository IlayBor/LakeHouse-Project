
import pyiceberg
from s3fs import S3FileSystem
import pyiceberg.catalog.rest

catalog = pyiceberg.catalog.rest.RestCatalog(
    name="catalog_name",
    uri="http://lakekeeper:8181/catalog",
    warehouse="lakehouse_warehouse",
)

s3fs = S3FileSystem(
    endpoint_url="http://minio:9000",
    key="ilaybor",
    secret="24342434",
)
