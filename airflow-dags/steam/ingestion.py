from datetime import datetime
from pipelines.common.connections import catalog, s3fs
from pipelines.steam.model import SteamGame

import requests
import logging
import time
import json

PATH = "warehouse/raw/steam_data"
FILE_NAME = "game_data"

BUCKET_NAME = "warehouse"


def load_missing_games(to_read_from_table_identifier):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    ingestion_date = datetime.now()
    max_games_allowed_in_batch = 10

    current_batch_data = []
    pages_in_current_batch = 0
    file_index = 1

    for steamappid in fetch_iceberg_table(to_read_from_table_identifier):
        game_data = get_steam_data(steamappid)
        if game_data:
            current_batch_data.append(game_data)
        pages_in_current_batch += 1

        if pages_in_current_batch >= max_games_allowed_in_batch:
            with s3fs.open(f"{PATH}/{ingestion_date.strftime('%Y/%m/%d')}/{FILE_NAME}_{file_index}.json", "w") as f:
                json.dump(current_batch_data, f)
            logging.info(f"Loaded batch {file_index}")

            current_batch_data = []
            pages_in_current_batch = 0
            file_index += 1

        time.sleep(1.8)

    if current_batch_data:
        logging.info(f"Flushing remains...")
        with s3fs.open(f"{PATH}/{ingestion_date.strftime('%Y/%m/%d')}/{FILE_NAME}_{file_index}.json", "w") as f:
            json.dump(current_batch_data, f)

def fetch_iceberg_table(to_read_from_table_identifier):
    table = catalog.load_table(to_read_from_table_identifier)
    scan_table = table.scan( selected_fields=("steam_app_id", )).to_arrow()
    for row in scan_table.to_pylist():
        steam_app_id = row["steam_app_id"]
        yield steam_app_id

def get_steam_data(steamappid):
    logging.info(f"Grabbing {steamappid} steam data.")
    url = f"https://store.steampowered.com/api/appdetails?appids={steamappid}&cc=tr"
    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()[steamappid]["data"]
        logging.info(f"Recieved game data")
        return data

    except Exception as e:
        logging.error(f"failed to load {steamappid} - {e}")
        return

