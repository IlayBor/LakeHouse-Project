import pyiceberg.catalog
import pyiceberg.catalog.rest
import pyiceberg.typedef
from pyiceberg.schema import Schema
from pyiceberg.types import (
    NestedField,
    StructType,
    ListType,
    StringType,
    BooleanType,
    IntegerType,
    LongType,
    DoubleType
)
import requests
import pyarrow as pa
import pandas as pd


catalog = pyiceberg.catalog.rest.RestCatalog(
    name="my_catalog_name",
    uri="http://lakekeeper:8181/catalog",
    warehouse="lakehouse_warehouse",
)

import pyarrow as pa

schema = pa.schema([
    pa.field("type", pa.string(), nullable=True),
    pa.field("name", pa.string(), nullable=True),
    pa.field("steam_appid", pa.int64(), nullable=False),
    pa.field("required_age", pa.int32(), nullable=True),
    pa.field("is_free", pa.bool_(), nullable=True),
    pa.field("controller_support", pa.string(), nullable=True),
    
    # List of Longs
    pa.field("dlc", pa.list_(pa.int64()), nullable=True),
    
    pa.field("detailed_description", pa.string(), nullable=True),
    pa.field("about_the_game", pa.string(), nullable=True),
    pa.field("short_description", pa.string(), nullable=True),
    
    # List of Structs
    pa.field("fullgame", pa.list_(
        pa.struct([
            pa.field("appid", pa.int32(), nullable=True),
            pa.field("name", pa.string(), nullable=True)
        ])
    ), nullable=True),
    
    pa.field("supported_languages", pa.string(), nullable=True),
    pa.field("header_image", pa.string(), nullable=True),
    pa.field("website", pa.string(), nullable=True),
    
    # Structs
    pa.field("pc_requirements", pa.struct([
        pa.field("minimum", pa.string(), nullable=True),
        pa.field("recommended", pa.string(), nullable=True)
    ]), nullable=True),
    
    pa.field("mac_requirements", pa.struct([
        pa.field("minimum", pa.string(), nullable=True),
        pa.field("recommended", pa.string(), nullable=True)
    ]), nullable=True),
    
    pa.field("linux_requirements", pa.struct([
        pa.field("minimum", pa.string(), nullable=True),
        pa.field("recommended", pa.string(), nullable=True)
    ]), nullable=True),
    
    pa.field("legal_notice", pa.string(), nullable=True),
    pa.field("developers", pa.list_(pa.string()), nullable=True),
    pa.field("publishers", pa.list_(pa.string()), nullable=True),
    
    pa.field("demos", pa.list_(
        pa.struct([
            pa.field("appid", pa.int64(), nullable=True),
            pa.field("description", pa.string(), nullable=True)
        ])
    ), nullable=True),
    
    pa.field("price_overview", pa.struct([
        pa.field("currency", pa.string(), nullable=True),
        pa.field("initial", pa.float64(), nullable=True),
        pa.field("final", pa.float64(), nullable=True),
        pa.field("discount_percent", pa.float64(), nullable=True),
        pa.field("initial_formatted", pa.string(), nullable=True),
        pa.field("final_formatted", pa.string(), nullable=True)
    ]), nullable=True),
    
    pa.field("packages", pa.list_(pa.int64()), nullable=True),
    
    pa.field("package_groups", pa.list_(
        pa.struct([
            pa.field("name", pa.string(), nullable=True),
            pa.field("title", pa.string(), nullable=True),
            pa.field("description", pa.string(), nullable=True),
            pa.field("selection_text", pa.string(), nullable=True),
            pa.field("save_text", pa.string(), nullable=True),
            pa.field("display_type", pa.int32(), nullable=True),
            pa.field("is_recurring_subscription", pa.string(), nullable=True),
            pa.field("subs", pa.list_(
                pa.struct([
                    pa.field("packageid", pa.int64(), nullable=True),
                    pa.field("percent_savings_text", pa.string(), nullable=True),
                    pa.field("percent_savings", pa.float64(), nullable=True),
                    pa.field("option_text", pa.string(), nullable=True),
                    pa.field("option_description", pa.string(), nullable=True),
                    pa.field("can_get_free_license", pa.string(), nullable=True),
                    pa.field("is_free_license", pa.bool_(), nullable=True),
                    pa.field("price_in_cents_with_discount", pa.int64(), nullable=True)
                ])
            ), nullable=True)
        ])
    ), nullable=True),
    
    pa.field("platforms", pa.struct([
        pa.field("windows", pa.bool_(), nullable=True),
        pa.field("mac", pa.bool_(), nullable=True),
        pa.field("linux", pa.bool_(), nullable=True)
    ]), nullable=True),
    
    pa.field("metacritic", pa.struct([
        pa.field("score", pa.int32(), nullable=True),
        pa.field("url", pa.string(), nullable=True)
    ]), nullable=True),
    
    pa.field("categories", pa.list_(
        pa.struct([
            pa.field("id", pa.int64(), nullable=True),
            pa.field("description", pa.string(), nullable=True)
        ])
    ), nullable=True),
    
    pa.field("genres", pa.list_(
        pa.struct([
            pa.field("id", pa.string(), nullable=True),
            pa.field("description", pa.string(), nullable=True)
        ])
    ), nullable=True),
    
    pa.field("screenshots", pa.list_(
        pa.struct([
            pa.field("id", pa.int64(), nullable=True),
            pa.field("path_thumbnail", pa.string(), nullable=True),
            pa.field("path_full", pa.string(), nullable=True)
        ])
    ), nullable=True),
    
    pa.field("movies", pa.list_(
        pa.struct([
            pa.field("id", pa.int64(), nullable=True),
            pa.field("name", pa.string(), nullable=True),
            pa.field("thumbnail", pa.string(), nullable=True),
            pa.field("webm", pa.struct([
                pa.field("480", pa.string(), nullable=True),
                pa.field("max", pa.string(), nullable=True)
            ]), nullable=True),
            pa.field("mp4", pa.struct([
                pa.field("480", pa.string(), nullable=True),
                pa.field("max", pa.string(), nullable=True)
            ]), nullable=True),
            pa.field("highlight", pa.bool_(), nullable=True)
        ])
    ), nullable=True),
    
    pa.field("recommendations", pa.struct([
        pa.field("total", pa.int32(), nullable=True)
    ]), nullable=True),
    
    pa.field("achievements", pa.struct([
        pa.field("total", pa.int32(), nullable=True),
        pa.field("highlighted", pa.list_(
            pa.struct([
                pa.field("name", pa.string(), nullable=True),
                pa.field("path", pa.string(), nullable=True)
            ])
        ), nullable=True)
    ]), nullable=True),
    
    pa.field("release_date", pa.struct([
        pa.field("coming_soon", pa.bool_(), nullable=True),
        pa.field("date", pa.string(), nullable=True)
    ]), nullable=True),
    
    pa.field("support_info", pa.struct([
        pa.field("url", pa.string(), nullable=True),
        pa.field("email", pa.string(), nullable=True)
    ]), nullable=True),
    
    pa.field("background", pa.string(), nullable=True),
    
    pa.field("content_descriptors", pa.struct([
        pa.field("ids", pa.list_(pa.int64()), nullable=True),
        pa.field("notes", pa.string(), nullable=True)
    ]), nullable=True)
])

iceberg_table = catalog.create_table_if_not_exists(
  identifier='bronze.test4',
  schema=schema
)

url = "https://store.steampowered.com/api/appdetails?appids=3900"
response = requests.get(url)
response.raise_for_status()
data = response.json()["3900"]["data"]

pa_table = pa.Table.from_pylist([data], schema=schema)
iceberg_table.append(pa_table)