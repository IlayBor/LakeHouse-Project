import requests
import json

# print("Creating Project...")
# with open('project.json', 'r') as f:
#     project_data = json.load(f)
# project_response = requests.post(f"http://lakekeeper:8181/management/v1/project", json=project_data)
# print("Created Project!")

HOST = "lakekeeper"

print("Accept TOS...")
tos_response = requests.post(f"http://{HOST}:8181/management/v1/bootstrap", json={"accept-terms-of-use": True})
print("Accepted!")

print("Creating Warehouse...")
with open('warehouse.json', 'r') as f:
    warehouse_data = json.load(f)
# warehouse_data["project-id"] = project_response.json()["project-id"]
response = requests.post(f"http://{HOST}:8181/management/v1/warehouse", json=warehouse_data)
print("Created Warehouse!")

print("Creating Namespace...")
print(response.json())
warehouse_id = response.json()['warehouse-id']
ns_response = requests.post(f"http://{HOST}:8181/catalog/v1/{warehouse_id}/namespaces", json={"namespace": ["default"]})
print("Created Namespace!")