# LakeHouse Project

End-to-end ELT pipeline built on an open lakehouse architecture. Game deal data is ingested from external APIs, landed as raw JSON in S3-compatible object storage, upserted into Apache Iceberg tables, transformed through a dbt modelling layer on Trino, and served to a Power BI dashboard -- all orchestrated by Apache Airflow.

## Architecture

```mermaid
flowchart LR
    subgraph Sources
        CS[CheapShark API]
        ST[Steam API]
    end

    subgraph Ingestion
        PY[Python Pipelines\nPydantic + Requests]
    end

    subgraph Storage
        S3[MinIO\nS3-Compatible Storage]
        ICE[Apache Iceberg\nLakeKeeper REST Catalog]
    end

    subgraph Transformation
        TR[Trino\nQuery Engine]
        DBT[dbt\nstaging → intermediate → marts]
    end

    subgraph BI
        PBI[Power BI\nDashboard]
    end

    CS --> PY
    ST --> PY
    PY -- raw JSON --> S3
    S3 -- PyIceberg upsert --> ICE
    ICE <--> TR
    TR <--> DBT
    DBT -- mart tables --> PBI

    AF[Apache Airflow + Cosmos]
    AF -. orchestrates .-> PY
    AF -. orchestrates .-> ICE
    AF -. orchestrates .-> DBT
```

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | Apache Airflow 3.1.6 + Astronomer Cosmos |
| Object Storage | MinIO (S3-compatible) |
| Table Format | Apache Iceberg |
| Iceberg Catalog | LakeKeeper (REST) |
| Query Engine | Trino |
| Transformations | dbt-trino |
| Data Validation | Pydantic |
| BI | Power BI |
| Infrastructure | Docker Compose |

## ELT Pipelines

**CheapShark Deals** -- Paginates through the CheapShark API, writes batched JSON files to MinIO, validates records with Pydantic, and upserts them into an Iceberg staging table. dbt then cleans, renames, and joins the data into analytics-ready mart tables.

**Steam Game Metadata** -- An incremental enrichment pipeline. A dbt intermediate model computes the set difference between CheapShark game IDs and already-fetched Steam metadata, producing a list of games still missing. Python fetches only those games from the Steam Store API, upserts them into Iceberg, and dbt builds marts that unnest genres, categories, developers, and publishers into normalized tables.

Both pipelines are fully orchestrated as Airflow DAGs with Cosmos running dbt models as native Airflow tasks.

## Project Structure

```
├── Lakehouse-Composes/    # Docker infrastructure (Lakehouse + Airflow stacks)
├── Lakehouse-Dags/        # Airflow DAGs, Python pipelines, dbt project
└── Lakehouse-Dashboard/   # Power BI dashboard
```

See each subfolder's README for detailed documentation.

## Getting Started

1. Add host entries for local development:
   ```
   127.0.0.1 minio
   127.0.0.1 trino
   ```
2. Start the Lakehouse stack (must start first):
   ```bash
   docker compose up                  # from Lakehouse-Composes/Lakehouse/
   ```
3. Start the Airflow stack:
   ```bash
   docker compose up -d --build       # from Lakehouse-Composes/Airflow/
   ```
4. Open the Airflow UI at [http://localhost:8090](http://localhost:8090) and trigger the DAGs.
