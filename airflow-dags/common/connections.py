import os
import pyiceberg
from s3fs import S3FileSystem
import pyiceberg.catalog.rest

# These tasks run INSIDE the Airflow worker container, so the endpoints must
# resolve on the shared Docker network ("shared-data-network"):
#   - LakeKeeper catalog -> lakekeeper:8181
#   - MinIO S3 API       -> minio:9000   (9000 is the in-container port; 6000 is
#                                          only the host-published mapping)
# To run the pipelines directly on the host instead, override via env vars, e.g.:
#   ICEBERG_CATALOG_URI=http://localhost:8181/catalog
#   S3_ENDPOINT_URL=http://localhost:6000
CATALOG_URI = os.environ.get("ICEBERG_CATALOG_URI", "http://lakekeeper:8181/catalog")
S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL", "http://minio:9000")

catalog = pyiceberg.catalog.rest.RestCatalog(
    name="catalog_name",
    uri=CATALOG_URI,
    warehouse="lakehouse_warehouse",
)

s3fs = S3FileSystem(
    endpoint_url=S3_ENDPOINT_URL,
    key="ilaybor",
    secret="24342434",
)
