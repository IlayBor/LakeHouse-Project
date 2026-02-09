import datetime
import pyiceberg.catalog
import pyiceberg.catalog.rest
import s3fs
import pyarrow as pa
from steam.schema import schema
from steam.model import SteamGame, SteamGames
from common.connections import connect_to_s3
from pydantic_to_pyarrow import get_pyarrow_schema

schema = get_pyarrow_schema(SteamGame)
print(schema)
catalog = pyiceberg.catalog.rest.RestCatalog(
    name="my_catalog_name",
    uri="http://lakekeeper:8181/catalog",
    warehouse="lakehouse_warehouse",
)

iceberg_table = catalog.create_table_if_not_exists(
    identifier="bronze.test4", schema=schema
)

s3 = s3fs.S3FileSystem(
    endpoint_url="http://minio:9000",
    key="ilaybor",
    secret="24342434",
)

today = datetime.datetime.now().strftime("%Y/%m/%d")
for path in s3.glob(f"warehouse/raw/steam_data/{today}/*.json"):
    with s3.open(path) as file:
        data = SteamGames.validate_json(file.read())
    data = [game.model_dump() for game in data]
    table = pa.Table.from_pylist(data, schema=schema)
    iceberg_table.upsert(table, ["steam_appid"])
