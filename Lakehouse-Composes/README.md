# Lakehouse Infrastructure

Two Docker Compose stacks that provision a complete open lakehouse platform -- from S3-compatible object storage to a distributed SQL query engine -- with fully automated bootstrap. No manual setup beyond `docker compose up`.

## Quick Start

A top-level `docker-compose.yml` orchestrates both stacks via Compose's native
[`include`](https://docs.docker.com/compose/how-tos/multiple-compose-files/include/)
directive, so the whole platform comes up with a single command:

```bash
docker compose up -d --build      # from Lakehouse-Composes/
```

This brings up the Lakehouse stack and the Airflow stack together as one Compose
project. Each child stack remains runnable on its own from its respective
subdirectory (`Lakehouse/` or `Airflow/`).

## Lakehouse Stack

Defined in `Lakehouse/docker-compose.yml`. Provides the core data platform services.


<img width="280" height="248" alt="image" src="https://github.com/user-attachments/assets/86de0c99-668b-46f9-9f53-dc613c3cca81" />


| Service | Image | Port | Role |
|---|---|---|---|
| MinIO | `minio/minio:latest` | 6000 (API) / 6001 (Console) | S3-compatible object storage for raw data and Iceberg data files |
| LakeKeeper | `lakekeeper/catalog:latest-main` | 8181 | Apache Iceberg REST catalog -- manages table metadata |
| Trino | `trinodb/trino:latest` | 8080 | Distributed SQL query engine over Iceberg tables |
| PostgreSQL | `postgres:17` | 5434 | Metadata store for LakeKeeper |

### Bootstrap Sequence

Three init containers run automatically on first startup, in order:

1. **`minio_create_default_bucket`** -- Creates the `warehouse` S3 bucket in MinIO using the MinIO CLI (`mc`).
2. **`lakekeeper-init`** (`init.py`) -- Bootstraps LakeKeeper: accepts the Terms of Service, creates the `lakehouse_warehouse` warehouse pointing to the MinIO bucket, and provisions three Iceberg namespaces: `staging`, `intermediate`, and `marts`. Each step is idempotent.
3. **Trino** starts once LakeKeeper and MinIO are healthy, configured via `iceberg.properties` to use LakeKeeper as its REST catalog and MinIO for S3 storage.

## Airflow Stack

Defined in `Airflow/docker-compose.yaml`. Provides workflow orchestration using the CeleryExecutor architecture.


<img width="351" height="191" alt="image" src="https://github.com/user-attachments/assets/2ad6c59f-1454-481d-ba42-ce8b586b8d87" />


The custom Airflow image (`Dockerfile`) extends `apache/airflow:3.1.6` with `dbt-trino`, `astronomer-cosmos`, `pyiceberg`, `pydantic`, `s3fs`, and other pipeline dependencies.

DAGs are synced from Git via the `apache-airflow-providers-git` bundle, tracking the `main` branch with a 120-second refresh interval, tracking sub folder called Lakehouse-Dags.

## Networking

Both stacks share a Docker bridge network named `shared-data-network`, declared
identically in each stack's compose file. When launched together via the
top-level `include`, Compose creates a single shared network for the combined
project; when a stack is launched on its own, it creates/joins the same named
network. This allows Airflow workers to reach MinIO, LakeKeeper, and Trino by
container hostname.
