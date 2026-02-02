MinIO - http://localhost:9001  
LakeKeeper - http://localhost:8181  
Trino - http://localhost:8080  
MetaBase - http://localhost:3000  
Airflow - http://localhost:8090 


You need to add minio and trino to your hosts file to run it locally (the actual ingestion script and dbt).
on windows - C:\Windows\System32\drivers\etc
as follows:
127.0.0.1 minio
127.0.0.1 trino


To run airflow compose (under ./airflow):
docker compose up

To run lakehouse compose (under ./lakehouse):
docker compose up

