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


catalog = pyiceberg.catalog.rest.RestCatalog(
    name="my_catalog_name",
    uri="http://lakekeeper:8181/catalog",
    warehouse="lakehouse_warehouse",
)

schema = Schema(
    NestedField(1, "type", StringType(), required=False),
    NestedField(2, "name", StringType(), required=False),
    NestedField(3, "steam_appid", LongType(), required=True),
    NestedField(4, "required_age", IntegerType(), required=False),
    NestedField(5, "is_free", BooleanType(), required=False),
    NestedField(6, "controller_support", StringType(), required=False),
    NestedField(7, "dlc", ListType(element_id=8, element=LongType(), element_required=False), required=False),
    NestedField(9, "detailed_description", StringType(), required=False),
    NestedField(10, "about_the_game", StringType(), required=False),
    NestedField(11, "short_description", StringType(), required=False),
    NestedField(12, "fullgame", ListType(
        element_id=13, 
        element=StructType(
            NestedField(14, "appid", IntegerType(), required=False),
            NestedField(15, "name", StringType(), required=False)
        ), 
        element_required=False
    ), required=False),
    NestedField(16, "supported_languages", StringType(), required=False),
    NestedField(17, "header_image", StringType(), required=False),
    NestedField(18, "website", StringType(), required=False),
    NestedField(19, "pc_requirements", StructType(
        NestedField(20, "minimum", StringType(), required=False),
        NestedField(21, "recommended", StringType(), required=False)
    ), required=False),
    NestedField(22, "mac_requirements", StructType(
        NestedField(23, "minimum", StringType(), required=False),
        NestedField(24, "recommended", StringType(), required=False)
    ), required=False),
    NestedField(25, "linux_requirements", StructType(
        NestedField(26, "minimum", StringType(), required=False),
        NestedField(27, "recommended", StringType(), required=False)
    ), required=False),
    NestedField(28, "legal_notice", StringType(), required=False),
    NestedField(29, "developers", ListType(element_id=30, element=StringType(), element_required=False), required=False),
    NestedField(31, "publishers", ListType(element_id=32, element=StringType(), element_required=False), required=False),
    NestedField(33, "demos", ListType(
        element_id=34, 
        element=StructType(
            NestedField(35, "appid", LongType(), required=False),
            NestedField(36, "description", StringType(), required=False)
        ), 
        element_required=False
    ), required=False),
    NestedField(37, "price_overview", StructType(
        NestedField(38, "currency", StringType(), required=False),
        NestedField(39, "initial", DoubleType(), required=False),
        NestedField(40, "final", DoubleType(), required=False),
        NestedField(41, "discount_percent", DoubleType(), required=False),
        NestedField(42, "initial_formatted", StringType(), required=False),
        NestedField(43, "final_formatted", StringType(), required=False)
    ), required=False),
    NestedField(44, "packages", ListType(element_id=45, element=LongType(), element_required=False), required=False),
    NestedField(46, "package_groups", ListType(
        element_id=47, 
        element=StructType(
            NestedField(48, "name", StringType(), required=False),
            NestedField(49, "title", StringType(), required=False),
            NestedField(50, "description", StringType(), required=False),
            NestedField(51, "selection_text", StringType(), required=False),
            NestedField(52, "save_text", StringType(), required=False),
            NestedField(53, "display_type", IntegerType(), required=False),
            NestedField(54, "is_recurring_subscription", StringType(), required=False),
            NestedField(55, "subs", ListType(
                element_id=56, 
                element=StructType(
                    NestedField(57, "packageid", LongType(), required=False),
                    NestedField(58, "percent_savings_text", StringType(), required=False),
                    NestedField(59, "percent_savings", DoubleType(), required=False),
                    NestedField(60, "option_text", StringType(), required=False),
                    NestedField(61, "option_description", StringType(), required=False),
                    NestedField(62, "can_get_free_license", StringType(), required=False),
                    NestedField(63, "is_free_license", BooleanType(), required=False),
                    NestedField(64, "price_in_cents_with_discount", LongType(), required=False)
                ), 
                element_required=False
            ), required=False)
        ), 
        element_required=False
    ), required=False),
    NestedField(65, "platforms", StructType(
        NestedField(66, "windows", BooleanType(), required=False),
        NestedField(67, "mac", BooleanType(), required=False),
        NestedField(68, "linux", BooleanType(), required=False)
    ), required=False),
    NestedField(69, "metacritic", StructType(
        NestedField(70, "score", IntegerType(), required=False),
        NestedField(71, "url", StringType(), required=False)
    ), required=False),
    NestedField(72, "categories", ListType(
        element_id=73, 
        element=StructType(
            NestedField(74, "id", LongType(), required=False),
            NestedField(75, "description", StringType(), required=False)
        ), 
        element_required=False
    ), required=False),
    NestedField(76, "genres", ListType(
        element_id=77, 
        element=StructType(
            NestedField(78, "id", StringType(), required=False),
            NestedField(79, "description", StringType(), required=False)
        ), 
        element_required=False
    ), required=False),
    NestedField(80, "screenshots", ListType(
        element_id=81, 
        element=StructType(
            NestedField(82, "id", LongType(), required=False),
            NestedField(83, "path_thumbnail", StringType(), required=False),
            NestedField(84, "path_full", StringType(), required=False)
        ), 
        element_required=False
    ), required=False),
    NestedField(85, "movies", ListType(
        element_id=86, 
        element=StructType(
            NestedField(87, "id", LongType(), required=False),
            NestedField(88, "name", StringType(), required=False),
            NestedField(89, "thumbnail", StringType(), required=False),
            NestedField(90, "webm", StructType(
                NestedField(91, "480", StringType(), required=False),
                NestedField(92, "max", StringType(), required=False)
            ), required=False),
            NestedField(93, "mp4", StructType(
                NestedField(94, "480", StringType(), required=False),
                NestedField(95, "max", StringType(), required=False)
            ), required=False),
            NestedField(96, "highlight", BooleanType(), required=False)
        ), 
        element_required=False
    ), required=False),
    NestedField(97, "recommendations", StructType(
        NestedField(98, "total", IntegerType(), required=False)
    ), required=False),
    NestedField(99, "achievements", StructType(
        NestedField(100, "total", IntegerType(), required=False),
        NestedField(101, "highlighted", ListType(
            element_id=102, 
            element=StructType(
                NestedField(103, "name", StringType(), required=False),
                NestedField(104, "path", StringType(), required=False)
            ), 
            element_required=False
        ), required=False)
    ), required=False),
    NestedField(105, "release_date", StructType(
        NestedField(106, "coming_soon", BooleanType(), required=False),
        NestedField(107, "date", StringType(), required=False)
    ), required=False),
    NestedField(108, "support_info", StructType(
        NestedField(109, "url", StringType(), required=False),
        NestedField(110, "email", StringType(), required=False)
    ), required=False),
    NestedField(111, "background", StringType(), required=False),
    NestedField(112, "content_descriptors", StructType(
        NestedField(113, "ids", ListType(element_id=114, element=LongType(), element_required=False), required=False),
        NestedField(115, "notes", StringType(), required=False)
    ), required=False)
)

iceberg_table = catalog.create_table_if_not_exists(
  identifier='bronze.test4',
  schema=schema
)

url = "https://store.steampowered.com/api/appdetails?appids=3900"
response = requests.get(url)
response.raise_for_status()
data = response.json()["3900"]["data"]
arrow_schema = schema.as_arrow()
pa_table = pa.Table.from_pylist([data], schema=arrow_schema)
print(pa_table)

table = catalog.load_table('bronze.test4')
table.append(pa_table)