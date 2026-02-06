from utils.utils import connect_to_duckdb
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def transform_to_iceberg(SOURCE_FILE, TARGET_SCHEME, TARGET_TABLE_NAME):
    con, LAKEKEEPER_CATALOG_NAME = connect_to_duckdb()
    
    SOURCE_FILE_FULL_PATH = f's3://{SOURCE_FILE}/**/*.json'
    TARGET_TABLE_PATH = LAKEKEEPER_CATALOG_NAME + '.' + TARGET_SCHEME + '.' + TARGET_TABLE_NAME
    logging.info(f"Trying to create table: {TARGET_TABLE_PATH} from file: {SOURCE_FILE}")

    try:
        create_table(con, TARGET_TABLE_PATH)
        logging.info("Table created / exists")

        upsert_into_table(con, SOURCE_FILE_FULL_PATH, TARGET_TABLE_PATH)
        logging.info("Data upserted successfully.")

        count = con.sql(f"SELECT COUNT(*) FROM {TARGET_TABLE_PATH}").fetchone()[0]
        logging.info(f"Success! Table {TARGET_TABLE_PATH} has {count} rows")

    except Exception as e:
        logging.error(f"transformation to iceberg failed for table {TARGET_TABLE_PATH}: {e}")
        raise e

def create_table(con, TARGET_TABLE_PATH):
    create_statment = f"""
        CREATE TABLE IF NOT EXISTS {TARGET_TABLE_PATH} (
            internalName VARCHAR,
            title VARCHAR,
            metacriticLink VARCHAR,
            dealID VARCHAR,
            storeID VARCHAR,
            gameID VARCHAR, 
            salePrice DOUBLE,
            normalPrice DOUBLE,
            isOnSale BOOLEAN,
            savings DOUBLE,
            metacriticScore INTEGER,
            steamRatingText VARCHAR,
            steamRatingPercent INTEGER,
            steamRatingCount INTEGER,
            steamAppID VARCHAR,
            releaseDate BIGINT,
            lastChange BIGINT,
            dealRating DOUBLE,
            thumb VARCHAR,
            ingestion_date DATE
        )   
    """
    con.sql(create_statment)

def upsert_into_table(con, SOURCE_FILE_FULL_PATH, TARGET_TABLE_PATH):
    insert_statment = f"""
        INSERT INTO {TARGET_TABLE_PATH}
        SELECT *, strftime(current_date, '%Y-%m-%d') as ingestion_date
        FROM read_json_auto('{SOURCE_FILE_FULL_PATH}');
    """
    remove_duplicates_statment = f"""
        DELETE FROM {TARGET_TABLE_PATH}
        WHERE (gameID, ingestion_date) IN (
            SELECT gameID, current_date
            FROM read_json_auto('{SOURCE_FILE_FULL_PATH}')
        )
    """

    try:
        con.begin()
        con.sql(remove_duplicates_statment)
        con.sql(insert_statment)
        con.commit()
    except Exception as e:
        con.rollback()
        raise e 