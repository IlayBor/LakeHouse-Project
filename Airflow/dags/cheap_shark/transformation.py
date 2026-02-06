from utils.utils import connect_to_duckdb
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def transform_to_iceberg(source_file, target_scheme, target_table_name):
    con, lakekeeper_catalog_name = connect_to_duckdb()
    
    source_file_path = f's3://{source_file}/**/*.json'
    target_table_path = lakekeeper_catalog_name + '.' + target_scheme + '.' + target_table_name
    logging.info(f"Trying to create table: {target_table_path} from file: {source_file}")

    try:
        create_table(con, target_table_path)
        logging.info("Table created / exists")

        upsert_into_table(con, source_file_path, target_table_path)
        logging.info("Data upserted successfully.")

        count = con.sql(f"SELECT COUNT(*) FROM {target_table_path}").fetchone()[0]
        logging.info(f"Success! Table {target_table_path} has {count} rows")

    except Exception as e:
        logging.error(f"transformation to iceberg failed for table {target_table_path}: {e}")
        raise e

def create_table(con, target_table_path):
    create_statment = f"""
        CREATE TABLE IF NOT EXISTS {target_table_path} (
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

def upsert_into_table(con, source_file_path, target_table_path):
    insert_statment = f"""
        INSERT INTO {target_table_path}
        SELECT *, strftime(current_date, '%Y-%m-%d') as ingestion_date
        FROM read_json_auto('{source_file_path}');
    """
    remove_duplicates_statment = f"""
        DELETE FROM {target_table_path}
        WHERE (gameID, ingestion_date) IN (
            SELECT gameID, current_date
            FROM read_json_auto('{source_file_path}')
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