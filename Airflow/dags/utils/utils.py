import duckdb
import logging

# returns connection to the lakehouse using duckdb
def connect_to_duckdb():
    S3_CATALOG_NAME = "s3_catalog" # Catalog name in DuckDB
    S3_ENDPOINT = "minio:9000" 
    S3_ACCESS_KEY = "ilaybor"
    S3_SECRET_KEY = "24342434"
    
    LAKEKEEPER_URI = "http://lakekeeper:8181" 
    LAKEKEEPER_CLIENT_ID = "ilaybor"
    LAKEKEEPER_CLIENT_SECRET = "24342434"
    LAKEKEEPER_CATALOG_NAME = "lakekeeper_catalog" # Catalog name in DuckDB
    LAKEKEEPER_WAREHOUSE = "lakehouse_warehouse"

    con = duckdb.connect()

    logging.info("Loading Iceberg and S3 extensions...")
    con.sql("INSTALL iceberg; LOAD iceberg;")
    con.sql("INSTALL httpfs; LOAD httpfs;")

    logging.info(f"Configuring S3 connection to {S3_ENDPOINT}...")
    con.sql(f"""
        CREATE SECRET {S3_CATALOG_NAME}_secret (
            TYPE S3,
            KEY_ID '{S3_ACCESS_KEY}',
            SECRET '{S3_SECRET_KEY}',
            ENDPOINT '{S3_ENDPOINT}',
            URL_STYLE 'path',
            USE_SSL false
        );
    """)

    logging.info(f"Connecting to Lakekeeper at {LAKEKEEPER_URI}...")
    con.sql(f"""
        CREATE SECRET {LAKEKEEPER_CATALOG_NAME}_secret (
        TYPE iceberg,
        CLIENT_ID '{LAKEKEEPER_CLIENT_ID}',
        CLIENT_SECRET '{LAKEKEEPER_CLIENT_SECRET}',
        TOKEN 'bearer_token'
        );
    """)
    
    logging.info(f"Attaching to warehouse {LAKEKEEPER_WAREHOUSE}...")
    try:
        con.sql(f"""
            ATTACH '{LAKEKEEPER_WAREHOUSE}' AS {LAKEKEEPER_CATALOG_NAME} (
                TYPE iceberg,
                ENDPOINT '{LAKEKEEPER_URI}/catalog',
                SECRET '{LAKEKEEPER_CATALOG_NAME}_secret'
            );
        """)
    except Exception as e:
        logging.error(f"Failed to attach: {e}")
        raise e
    
    return con