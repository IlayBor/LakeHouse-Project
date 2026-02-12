from datetime import datetime
from pipelines.common.connections import s3fs

import requests
import logging
import time
import json


PATH = "warehouse/raw/cheapshark_data"
FILE_NAME = "deals"

def load_cheapshark_pages(start_page=0, end_page=None):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    ingestion_date = datetime.now()
    max_pages_allowed_in_batch = 10

    current_batch_data = []
    pages_in_current_batch = 0
    file_index = 1

    for page_data in fetch_deals_pages(start_page, end_page):
        current_batch_data.extend(page_data)
        pages_in_current_batch += 1
        if pages_in_current_batch >= max_pages_allowed_in_batch:
            with s3fs.open(f"{PATH}/{ingestion_date.strftime('%Y/%m/%d')}/{FILE_NAME}_{file_index}.json", "w") as f:
                json.dump(current_batch_data, f)
            logging.info(f"Loaded batch {file_index}")

            current_batch_data = []
            pages_in_current_batch = 0
            file_index += 1

    if current_batch_data:
        logging.info(f"Flushing remains...")
        with s3fs.open(f"{PATH}/{ingestion_date.strftime('%Y/%m/%d')}/{FILE_NAME}_{file_index}.json", "w") as f:
            json.dump(current_batch_data, f)

    logging.info(f"Ingestion completed.")


def fetch_deals_pages(start_page, end_page):
    current_page = start_page
    while True:
        if end_page is not None and current_page >= end_page:
            logging.info(f"Finished loading at page {current_page}")
            break

        try:
            logging.info(f"Fetching page {current_page}")
            url = f"https://www.cheapshark.com/api/1.0/deals?storeID=1&pageNumber={current_page}"
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            if not data:
                logging.info("Empty page received. Stopping fetch.")
                break

            yield data

            time.sleep(1.8)
            current_page += 1

        except requests.exceptions.RequestException as e:
            if response.status_code == 429:
                logging.error(
                    f"Got timeout error, must wait :{response.headers.get('Retry-After')} seconds"
                )
                raise e

            logging.error(f"Got error on page {current_page}: {e}")
            break

