from common.connections import connect_to_lakekeeper
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def transform_to_iceberg(source_file, target_table_scheme, target_table_name):
    catalog = connect_to_lakekeeper()

    source_file_path = f"s3://{source_file}/**/*.json"
    target_table_path = (
        lakekeeper_catalog_name + "." + target_table_scheme + "." + target_table_name
    )
    logging.info(
        f"Trying to create table: {target_table_path} from file: {source_file}"
    )

    try:
        catalog = connect_to_lakekeeper()
        logging.info("Table created / exists")

        upsert_into_table(con, source_file_path, target_table_path)
        logging.info("Data upserted successfully.")

        count = con.sql(f"SELECT COUNT(*) FROM {target_table_path}").fetchone()[0]
        logging.info(f"Success! Table {target_table_path} has {count} rows")

    except Exception as e:
        logging.error(
            f"transformation to iceberg failed for table {target_table_path}: {e}"
        )
        raise e


def create_table(con, source_file_path, target_table_path):
    create_statment = f"""
        CREATE TABLE IF NOT EXISTS {target_table_path} AS 
        SELECT *
        FROM read_json_auto('{source_file_path}')
    """
    con.sql(create_statment)


def upsert_into_table(con, source_file_path, target_table_path):
    insert_statment = f"""
        INSERT INTO {target_table_path}
        SELECT *, strftime(current_date, '%Y-%m-%d') as ingestion_date
        FROM read_json_auto('{source_file_path}');
    """
    try:
        con.sql(insert_statment)
    except Exception as e:
        raise e


transform_to_iceberg("warehouse/raw/steam_data", "bronze", "test4")
