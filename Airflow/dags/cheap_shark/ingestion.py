from datetime import datetime
from utils.utils import connect_to_s3

import requests
import logging
import time
import json

LOAD_PATH = "raw/cheapshark_data"
FILE_NAME = "deals"

BUCKET_NAME = "warehouse"

def load_cheapshark_pages(start_page = 0, end_page = None):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    s3 = connect_to_s3()
    
    ingestion_date = datetime.now()
    max_pages_allowed_in_batch = 10

    current_batch_data = [] 
    pages_in_current_batch = 0 
    file_index = 1

    for page_data in fetch_deals_pages(start_page, end_page):
        current_batch_data.extend(page_data)
        pages_in_current_batch += 1

        if pages_in_current_batch >= max_pages_allowed_in_batch:
            upload_to_s3(s3, BUCKET_NAME, current_batch_data, f"{LOAD_PATH}/{ingestion_date.strftime("%Y/%m/%d")}/{FILE_NAME}_{file_index}.json")
            logging.info(f"Loaded batch {file_index}")
            
            current_batch_data = []
            pages_in_current_batch = 0
            file_index += 1

    if current_batch_data:
        logging.info(f"Flushing remains...")
        upload_to_s3(s3, BUCKET_NAME, current_batch_data, f"{LOAD_PATH}/{ingestion_date.strftime("%Y/%m/%d")}/{FILE_NAME}_{file_index}.json")

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

            logging.error(response.headers.get("Retry-After"))

            response.raise_for_status()

            data = response.json()
            if not data:
                logging.info("Empty page received. Stopping fetch.")
                break

            yield data

            time.sleep(1.5)
            current_page +=1

        except requests.exceptions.RequestException as e:

            logging.error(f"Got error on page {current_page}: {e}")
            break

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
