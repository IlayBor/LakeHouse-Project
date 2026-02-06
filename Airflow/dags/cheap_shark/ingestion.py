from datetime import datetime

import requests
import logging
import boto3
import time
import json

MINIO_ENDPOINT = "http://minio:9000"
ACCESS_KEY = "ilaybor" 
SECRET_KEY = "24342434"
BUCKET_NAME = "warehouse"

LOAD_PATH = "raw/cheapshark_data"
FILE_NAME = "deals"

def load_cheapshark_pages(start, end = 0):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    s3 = boto3.client('s3',endpoint_url=MINIO_ENDPOINT,aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    
    current_date = datetime.now()
    batch_number = 10

    combined_data = [] 
    pages_counter = 0 
    load_file_index = 1

    for page_data in pages_generator(start, end):
        combined_data.extend(page_data)
        pages_counter += 1    
        if pages_counter >= batch_number:
            upload_to_s3(s3, BUCKET_NAME, combined_data, f"{LOAD_PATH}/{current_date.year}/{current_date.month}/{current_date.day}/{FILE_NAME}_{load_file_index}.json")
            logging.info(f"Loaded batch {load_file_index}!")
            combined_data = []
            pages_counter = 0
            load_file_index += 1
        time.sleep(1.5)

    if combined_data:
        logging.info(f"Flushing remains...")
        upload_to_s3(s3, BUCKET_NAME, combined_data, f"{LOAD_PATH}/{current_date.year}/{current_date.month}/{current_date.day}/{FILE_NAME}_{load_file_index}.json")

def pages_generator(start, end = 0):
    page = start
    while True:
        logging.info(f"Fetching page {page}")
        url = f"https://www.cheapshark.com/api/1.0/deals?storeID=1&pageNumber={page}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            yield data
        except requests.exceptions.RequestException as err:
            logging.error(f"Ended on page {page} - {err}")
            break
        
        page += 1
        if end and page >= end:
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
