import duckdb
import logging

S3_CATALOG_NAME = "s3_catalog" # Catalog name in DuckDB
S3_ENDPOINT = "minio:9000" 
S3_ACCESS_KEY = "ilaybor"
S3_SECRET_KEY = "24342434"
S3_BUCKET = "warehouse"

LAKEKEEPER_URI = "http://lakekeeper:8181" 
LAKEKEEPER_CLIENT_ID = "ilaybor"
LAKEKEEPER_CLIENT_SECRET = "24342434"
LAKEKEEPER_CATALOG_NAME = "lakekeeper_catalog" # Catalog name in DuckDB
LAKEKEEPER_WAREHOUSE = "lakehouse_warehouse"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def transform_to_iceberg(SOURCE_FILE, TARGET_SCHEME, TARGET_TABLE_NAME):
    
    TARGET_TABLE_PATH = LAKEKEEPER_CATALOG_NAME + '.' + TARGET_SCHEME + '.' + TARGET_TABLE_NAME
    logging.info(f"Source file:{SOURCE_FILE} Target Table Path: {TARGET_TABLE_PATH}")

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
        return 
    
    logging.info(f"Trying to create table...")
    SOURCE_FILE_FULL_PATH = f's3://{S3_BUCKET}/{SOURCE_FILE}/**/*.json'
    try:
        query = f"""
            CREATE TABLE {TARGET_TABLE_PATH} AS 
            SELECT *, strftime(current_date, '%Y-%m-%d') as ingestion_date
            FROM read_json_auto('{SOURCE_FILE_FULL_PATH}');
            """
        con.sql(query)
        logging.info(f"Created table!")
    except Exception as e:
        if "already exists" in str(e).lower():
            query = f"""
            INSERT INTO {TARGET_TABLE_PATH}
            SELECT *, strftime(current_date, '%Y-%m-%d') as ingestion_date
            FROM read_json_auto('{SOURCE_FILE_FULL_PATH}');
            """
            logging.warning(f"Table already exists... Inserting into it instead.")
            try:
                con.sql(query)
            except Exception as e:
                logging.error(f"Failed to insert into table {TARGET_TABLE_PATH}: {e}")
                raise e
        else:
            logging.error(f"Failed To create table {TARGET_TABLE_PATH}: {e}")
            raise e
    
    try:
        count = con.sql(f"SELECT COUNT(*) FROM {TARGET_TABLE_PATH}").fetchone()[0]
        logging.info(f"Success! Table {TARGET_TABLE_PATH} has {count} rows")
    except Exception as e:
        logging.error(f"Failed to count rows: {e}")
        raise e
