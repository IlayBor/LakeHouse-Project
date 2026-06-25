import requests
import json
import logging

HOST = "lakekeeper"
BASE_URL = f"http://{HOST}:8181"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def init():
    # Accepting TOS
    logging.info("Trying to accept TOS...")
    try:
        tos_response = requests.post(f"{BASE_URL}/management/v1/bootstrap", json={"accept-terms-of-use": True})
        tos_response.raise_for_status()
        logging.info("Accepted!")
    except requests.exceptions.RequestException as err:
        error_data = err.response.json()['error']
        if error_data['type'] == 'CatalogAlreadyBootstrapped':
            logging.warning("Boostrapped already, moving on...")
            pass
        else:
            logging.error(f"Boostrap failure: {error_data['code']} {error_data['message']}")
            return

    # Creating Warehouse
    with open('warehouse.json', 'r') as f:
        warehouse_data = json.load(f)
    try:
        logging.info("Creating Warehouse...")
        warehouse_response = requests.post(f"{BASE_URL}/management/v1/warehouse", json=warehouse_data)
        warehouse_response.raise_for_status()
        warehouse_id = warehouse_response.json()['warehouse-id']
        logging.info("Created Warehouse!")
    except requests.exceptions.RequestException as err:
        error_data = err.response.json()['error']
        if error_data['type'] == 'CreateWarehouseStorageProfileOverlap':
            warehouse_response = requests.get(f"{BASE_URL}/management/v1/warehouse")
            warehouse_id = warehouse_response.json()['warehouses'][0]['warehouse-id']
            logging.warning("Warehouse already created, moving on...")
            pass
        else:
            logging.error(f"Warehouse Creation Failure: {error_data['code']} {error_data['message']}")
            return
        
    # Creating Namespace
    namespaces = ["staging", "intermediate", "marts"]
    for ns in namespaces:
        payload={"namespace": [ns], "properties": {"location": f"s3://warehouse/{ns}"}}
        try:
            logging.info("Creating Namespace...")
            ns_response = requests.post(f"{BASE_URL}/catalog/v1/{warehouse_id}/namespaces", json=payload)
            ns_response.raise_for_status()
            logging.info(f"Created Namespace {ns}!")
        except requests.exceptions.RequestException as err:
            error_data = err.response.json()['error']
            if error_data['type'] == 'AlreadyExistsException':
                logging.warning("Namespace already created for this warehouse, moving on...")
                pass
            else:    
                logging.error(f"Namespace Creation Failure: {error_data['code']} {error_data['message']}")
                return

if __name__ == "__main__":
    init()