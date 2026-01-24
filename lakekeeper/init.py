import requests
import json

HOST = "lakekeeper"

print("Accept TOS...")
tos_response = requests.post(f"http://{HOST}:8181/management/v1/bootstrap", json={"accept-terms-of-use": True})
print("Accepted!")

print("Creating Warehouse...")
with open('warehouse.json', 'r') as f:
    warehouse_data = json.load(f)
response = requests.post(f"http://{HOST}:8181/management/v1/warehouse", json=warehouse_data)
print("Created Warehouse!")

print("Creating Namespace...")
print(response.json())
warehouse_id = response.json()['warehouse-id']
ns_response = requests.post(f"http://{HOST}:8181/catalog/v1/{warehouse_id}/namespaces", json={"namespace": ["default"]})
print("Created Namespace!")