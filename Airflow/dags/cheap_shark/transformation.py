from common.transform import transform_to_iceberg
from cheap_shark.model import GameDeal
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def transform_to_iceberg2(source_file, target_table):
    logging.info(f"Trying to create table: {target_table} from file: {source_file}")

    try:
        transform_to_iceberg(
            GameDeal, source_file, target_table, ["steamAppID", "ingestionDate"]
        )

    except Exception as e:
        logging.error(f"transformation to iceberg failed for table {target_table}: {e}")
        raise e
