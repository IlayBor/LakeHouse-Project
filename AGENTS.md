# AGENTS.md

## Project Overview
LakeHouse ELT pipeline: CheapShark/Steam APIs -> MinIO (S3) -> Apache Iceberg -> dbt (Trino) -> Power BI.
Orchestrated by Apache Airflow 3.1.6 with Astronomer Cosmos for dbt integration.

## Repository Structure
- `Lakehouse-Composes/` - Docker infrastructure (two compose stacks)
- `Lakehouse-Dags/` - Application code: Airflow DAGs, Python pipelines, dbt project
- `Lakehouse-Dashboard/` - Power BI dashboard (.pbix)

### Key Paths
- Python pipelines: `Lakehouse-Dags/pipelines/{common,cheapshark,steam}/`
- dbt project: `Lakehouse-Dags/dbt_project/`
- dbt models: `Lakehouse-Dags/dbt_project/models/{staging,intermediate,marts}/`
- Docker (top-level orchestrator): `Lakehouse-Composes/docker-compose.yml`
- Docker (Lakehouse): `Lakehouse-Composes/Lakehouse/docker-compose.yml`
- Docker (Airflow): `Lakehouse-Composes/Airflow/docker-compose.yaml`

## Infrastructure Commands
### Start everything (recommended)
A top-level compose orchestrates both stacks via Compose's `include` directive.
```bash
docker compose up -d --build            # from Lakehouse-Composes/
```
### Start an individual stack (still supported)
```bash
docker compose up                       # from Lakehouse-Composes/Lakehouse/
docker compose up -d --build            # from Lakehouse-Composes/Airflow/
```
### Service URLs
- Airflow: http://localhost:8090
- MinIO Console: http://localhost:6001 (API: 6000)
- LakeKeeper: http://localhost:8181
- Trino: http://localhost:8080

### Host file entries required for local dev
```
127.0.0.1 minio
127.0.0.1 trino
```

## Build Commands
### Docker
```bash
docker compose build                    # Rebuild Airflow image (from Lakehouse-Composes/Airflow/)
```
### Python Dependencies
Defined in `Lakehouse-Composes/Airflow/requirements.txt`. Installed inside Docker image.
Key packages: dbt-trino, astronomer-cosmos, pyiceberg, pydantic, s3fs, pydantic_to_pyarrow

### dbt
All dbt commands run from `Lakehouse-Dags/dbt_project/` (or via Cosmos in Airflow).
```bash
dbt run                                          # Run all models
dbt run --select stg_cheapshark_api__game_deals   # Run a single model
dbt run --select +stg_cheapshark_api__game_deals  # Run model and its upstream deps
dbt run --select staging.*                        # Run all models in a folder/schema
dbt test                                          # Run all tests
dbt test --select stg_cheapshark_api__game_deals  # Test a single model
dbt compile                                       # Compile models (validate SQL)
dbt debug                                         # Test dbt connection to Trino
```
Profile: `lakehouse_profile` connecting to Trino (iceberg catalog) at `10.0.0.96:8080`.

## Testing
No Python tests or dbt tests currently exist. The `dbt_project/tests/` directory is empty.
When adding tests:
- Python: use pytest, place tests in a `tests/` directory mirroring `pipelines/` structure
- dbt: add schema tests in `_<source>__models.yml` files or singular tests in `dbt_project/tests/`

## Python Code Style

### Imports
Order: stdlib -> third-party -> local (relative for same package, absolute for cross-package).
```python
from datetime import datetime                      # stdlib
from pipelines.common.connections import s3fs      # local absolute
from .connections import catalog, s3fs             # local relative (within same package)
```

### Naming
- **Files**: `snake_case.py`. DAG files prefixed with `DAG_` (e.g., `DAG_cheapshark.py`)
- **Functions**: `snake_case` (e.g., `upsert_iceberg_table`, `load_cheapshark_pages`)
- **Variables**: `snake_case` (e.g., `current_batch_data`, `file_index`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `PATH`, `FILE_NAME`, `BUCKET_NAME`)
- **Classes**: `PascalCase` (e.g., `GameDeal`, `SteamGame`, `PriceOverview`)

### Type Annotations
- Use Python 3.10+ union syntax: `str | None` (not `Optional[str]`)
- Use `list[str]` lowercase for generics (not `List[str]`) except in Pydantic models where `List[...]` from typing may appear
- Type function parameters and return values: `def func(model: BaseModel, path: str) -> None:`

### Pydantic Models
- Each data source has a `model.py` with Pydantic BaseModel classes
- Fields default to `None` with `| None = None` for optional API response fields
- Primary key fields have no default (required): e.g., `dealID: str`, `steam_appid: int`
- Use `Field(default_factory=...)` for computed defaults
- Use `Annotated[..., BeforeValidator(...)]` for custom validation
- Models map 1:1 to API response structure; nested objects get their own model class

### Error Handling
- Use `try/except` around HTTP requests with `response.raise_for_status()`
- Catch specific exceptions: `requests.exceptions.RequestException`
- Log errors with `logging.error()`, not print
- For non-critical failures (e.g., single game fetch), log and continue
- For rate limits (429), log and re-raise

### Logging
- Use the `logging` module (not print)
- Configure at function entry: `logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")`
- Use f-strings in log messages

### Pipeline Pattern
Each data source follows this structure:
```
pipelines/<source>/
  DAG_<source>.py   - Airflow DAG definition
  ingestion.py      - API fetching + JSON writing to MinIO
  model.py          - Pydantic data models
```
The DAG wires tasks as: `ingest -> upsert_iceberg_table -> dbt_transform`

Common utilities in `pipelines/common/`:
- `connections.py` - PyIceberg catalog and S3FileSystem singletons
- `transform.py` - Generic `upsert_iceberg_table()` function
- `__init__.py` - Re-exports `upsert_iceberg_table`, `catalog`, `s3fs`

### Ingestion Pattern
- Fetch data in pages/batches from APIs
- Write batches as JSON to MinIO: `warehouse/raw/<source>/{YYYY/MM/DD}/<name>_{index}.json`
- Rate-limit with `time.sleep(1.8)` between API calls
- Use generators (`yield`) for paginated fetches

## dbt / SQL Code Style

### Model Naming
- Staging: `stg_<source>__<entity>` (double underscore separator)
- Intermediate: `int_<description>`
- Marts: descriptive name (e.g., `deals`, `games_genres`)

### SQL Conventions
- Keywords: lowercase preferred (`select`, `from`, `with`, `as`, `where`)
- Type-casting keywords: uppercase (`CAST`, `AS`, `VARCHAR`)
- CTEs: use `with source as (...), renamed as (...) select * from renamed` pattern in staging
- Indentation: 4 spaces inside CTEs and select lists
- Column names: `snake_case`; rename from camelCase in staging layer
- Boolean columns: prefix with `is_` (e.g., `is_free`, `is_on_sale`)
- Group columns with comment headers: `-- ids`, `-- strings`, `-- numeric`, `-- booleans`, `-- dates`, `-- arrays & structs`
- Array flattening in marts: `CROSS JOIN UNNEST(array_col) AS t(col1, col2)`
- Jinja refs: `{{ ref("model_name") }}` (double quotes), `{{ source('source', 'table') }}` (single quotes)

### dbt YAML Files
- Sources: `_<source>__sources.yml` with column descriptions
- Models: `_<source>__models.yml` with column descriptions grouped by type (IDs, Strings, Numeric, etc.)
- Intermediate: `_int__models.yml`

### Materialization
Configured in `dbt_project.yml` (not per-model unless overriding):
- staging: `view`
- intermediate: `view` (override to `table` with `{{ config(materialized='table') }}` when needed)
- marts: `table`

### Custom Schema Macro
`macros/get_custom_schema.sql` overrides dbt default: uses `custom_schema_name` directly (no prefix).
Schemas map to: `staging`, `intermediate`, `marts` in the `iceberg` catalog.

## Airflow DAG Conventions
- Use context manager: `with DAG(...) as dag:`
- DAG IDs: descriptive snake_case (e.g., `get_cheapshark_deals`)
- Tags: `["steam-etl"]`
- `schedule=None`, `catchup=False` for manually triggered DAGs
- Use `PythonOperator` for ingestion and Iceberg operations
- Use Astronomer Cosmos `DbtTaskGroup` / `DbtRunLocalOperator` for dbt steps
- Chain tasks with `>>` operator
- dbt profile config defined per-DAG file using `ProfileConfig` + `TrinoBaseProfileMapping`

## Security Notes
- Credentials are currently hardcoded (MinIO, Trino, PostgreSQL). Do NOT add new hardcoded secrets.
- The `.env` file is tracked in git. Be cautious with sensitive values.
