from datetime import datetime
from utils.utils import connect_to_s3, connect_to_duckdb

import requests
import logging
import time
import json

LOAD_PATH = "raw/steam_data"
FILE_NAME = "game_data"

BUCKET_NAME = "warehouse"

def main(table_scheme, table_name):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    s3 = connect_to_s3()

    ingestion_date = datetime.now()
    max_games_allowed_in_batch = 10

    current_batch_data = [] 
    pages_in_current_batch = 0 
    file_index = 1

    for steamappid in fetch_iceberg_table(table_scheme, table_name):
        game_data = get_steam_data(steamappid)
        current_batch_data.append(game_data)
        pages_in_current_batch += 1

        if pages_in_current_batch >= max_games_allowed_in_batch:
            upload_to_s3(s3, BUCKET_NAME, current_batch_data, f"{LOAD_PATH}/{ingestion_date.strftime("%Y/%m/%d")}/{FILE_NAME}_{file_index}.json")
            logging.info(f"Loaded batch {file_index}")

            current_batch_data = []
            pages_in_current_batch = 0
            file_index += 1
            
        time.sleep(1.8)

    if current_batch_data:
        logging.info(f"Flushing remains...")
        upload_to_s3(s3, BUCKET_NAME, current_batch_data, f"{LOAD_PATH}/{ingestion_date.strftime("%Y/%m/%d")}/{FILE_NAME}_{file_index}.json")
    
def fetch_iceberg_table(table_scheme, table_name):
    con, lakekeeper_catalog_name = connect_to_duckdb()
    target_table_path = lakekeeper_catalog_name + '.' + table_scheme + '.' + table_name

    query = f"SELECT steamappid from {target_table_path}"
    cursor = con.execute(query)

    while True:
        row = cursor.fetchone()
        if row is None:
            break

        yield row[0]

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

def upload_to_s3(s3, bucket_name, data, key):
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body= json.dumps(data)
        )
        logging.info("Uploaded data successfuly!")
    except Exception as e:
        logging.error(f"Couldnt upload to s3: {e}")
        raise e

main("bronze", "cheapshark_data")