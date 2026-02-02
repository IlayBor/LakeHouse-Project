# Tools
These are the main tools of the project  
**Airflow** - http://localhost:8090  
**MinIO** - http://localhost:9001  
**LakeKeeper** - http://localhost:8181  
**MetaBase** - http://localhost:3000  
**Trino** - http://localhost:8080  


## How to run locally
You need to add minio and trino to your hosts file to run it locally (the actual ingestion script and dbt).  
on windows - **C:\Windows\System32\drivers\etc** as follows:  
127.0.0.1 minio  
127.0.0.1 trino  

## Docker composes
currently there are two docker composes:
1. for the **lakehouse architecture** (lakekeeper + minio + trino + metabase and their dependencies (postgres, redis etc..)  
To run this just cd into *./lakehouse* and run *docker compose up* 

2. for the **orchestration + transformation** (airflow + dbt)
To run this just cd into *./airflow* and run *docker compose up -d --build* 

**you must run the lakehouse architecture compose before running the orchestration + transformation compose.**