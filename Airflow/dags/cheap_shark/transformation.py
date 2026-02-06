from utils.utils import connect_to_duckdb
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def transform_to_iceberg(SOURCE_FILE, TARGET_SCHEME, TARGET_TABLE_NAME):
    LAKEKEEPER_CATALOG_NAME = "lakekeeper_catalog"
    con = connect_to_duckdb()

    TARGET_TABLE_PATH = LAKEKEEPER_CATALOG_NAME + '.' + TARGET_SCHEME + '.' + TARGET_TABLE_NAME
    logging.info(f"Source file:{SOURCE_FILE} Target Table Path: {TARGET_TABLE_PATH}")

    logging.info(f"Trying to create table...")
    SOURCE_FILE_FULL_PATH = f's3://{SOURCE_FILE}/**/*.json'
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
