import pyarrow as pa
from pydantic_to_pyarrow import get_pyarrow_schema
from .connections import catalog, s3fs
from pydantic import BaseModel
from datetime import datetime
import json


def upsert_iceberg_table(
    model: BaseModel, folder_path: str, table_identifier: str, primary_key: list[str]
) -> None:

    today = datetime.now().strftime("%Y/%m/%d")
    schema = get_pyarrow_schema(model)

    iceberg_table = catalog.create_table_if_not_exists(
        identifier=table_identifier, schema=schema
    )
    
    for path in s3fs.glob(f"{folder_path}/{today}/*.json"):
        with s3fs.open(path) as file:
            data = json.load(file)
        data = [model(**obj).model_dump() for obj in data[:121]]
        table = pa.Table.from_pylist(data, schema=schema)
        iceberg_table.upsert(table, primary_key)
