import os
import pyiceberg
from s3fs import S3FileSystem
import pyiceberg.catalog.rest

CATALOG_URI = os.environ.get("ICEBERG_CATALOG_URI") or os.environ["CATALOG_URI"]
S3_ENDPOINT_URL = os.environ["S3_ENDPOINT_URL"]
CATALOG_WAREHOUSE = os.environ["CATALOG_WAREHOUSE"]
S3_ACCESS_KEY = os.environ["AWS_ACCESS_KEY_ID"]
S3_SECRET_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]

catalog = pyiceberg.catalog.rest.RestCatalog(
    name="catalog_name",
    uri=CATALOG_URI,
    warehouse=CATALOG_WAREHOUSE,
)

s3fs = S3FileSystem(
    endpoint_url=S3_ENDPOINT_URL,
    key=S3_ACCESS_KEY,
    secret=S3_SECRET_KEY,
)
