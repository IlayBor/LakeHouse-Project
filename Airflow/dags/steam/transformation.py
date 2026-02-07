from utils.utils import connect_to_duckdb
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def transform_to_iceberg(source_file, target_table_scheme, target_table_name):
    con, lakekeeper_catalog_name = connect_to_duckdb()
    
    source_file_path = f's3://{source_file}/**/*.json'
    target_table_path = lakekeeper_catalog_name + '.' + target_table_scheme + '.' + target_table_name
    logging.info(f"Trying to create table: {target_table_path} from file: {source_file}")

    try:
        create_table(con, target_table_path)
        logging.info("Table created / exists")

        # upsert_into_table(con, source_file_path, target_table_path)
        # logging.info("Data upserted successfully.")

        # count = con.sql(f"SELECT COUNT(*) FROM {target_table_path}").fetchone()[0]
        # logging.info(f"Success! Table {target_table_path} has {count} rows")

    except Exception as e:
        logging.error(f"transformation to iceberg failed for table {target_table_path}: {e}")
        raise e

def create_table(con, target_table_path):
    create_statment = f"""
        CREATE TABLE IF NOT EXISTS {target_table_path} (
            type VARCHAR,
            name VARCHAR,
            steam_appid INTEGER,
            required_age INTEGER,
            is_free BOOLEAN,
            controller_support VARCHAR,
            dlc VARCHAR, 
            detailed_description VARCHAR,
            about_the_game VARCHAR,
            short_description VARCHAR,
            supported_languages VARCHAR,
            reviews VARCHAR,
            header_image VARCHAR,
            capsule_image VARCHAR,
            capsule_imagev5 VARCHAR,
            website VARCHAR,
            pc_requirements STRUCT(minimum VARCHAR, recommended VARCHAR),
            mac_requirements STRUCT(minimum VARCHAR, recommended VARCHAR),
            linux_requirements STRUCT(minimum VARCHAR, recommended VARCHAR),
            legal_notice VARCHAR,
            developers VARCHAR[],
            publishers VARCHAR,
            demos VARCHAR, 
            price_overview VARCHAR,
            packages VARCHAR,
            package_groups VARCHAR,
            platforms VARCHAR,
            metacritic VARCHAR,
            categories VARCHAR,
            genres VARCHAR,
            screenshots VARCHAR,
            movies VARCHAR,
            recommendations VARCHAR,
            achievements VARCHAR,
            release_date VARCHAR,
            support_info VARCHAR,
            background VARCHAR,
            background_raw VARCHAR,
            content_descriptors VARCHAR,
            ratings VARCHAR, 
            drm_notice VARCHAR,
            ext_user_account_notice VARCHAR,
            ingestion_date DATE
        );
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
    
transform_to_iceberg("warehouse/raw/steam_data", "bronze", "steam_data")