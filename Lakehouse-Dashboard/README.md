# Steam Deals Dashboard

Power BI dashboard providing interactive analytics over the lakehouse marts layer. Connects directly to the Trino query engine, which reads from Apache Iceberg tables in MinIO -- giving Power BI access to the full open lakehouse without any data extracts or imports.

## Data Sources

The dashboard queries the following mart tables via Trino (`iceberg.marts` schema):

| Mart Table | Description |
|---|---|
| `deals` | Enriched game deals -- CheapShark pricing and deal ratings joined with Steam metadata (name, description, platform support, Metacritic score, release date) |
| `games_genres` | Game-to-genre mapping (e.g., Action, RPG, Free to Play) |
| `games_categories` | Game-to-category mapping (e.g., Multiplayer, Steam Achievements, Controller Support) |
| `game_developers` | Game-to-developer mapping |
| `game_publishers` | Game-to-publisher mapping |

## Dashboard Preview

<!-- Add a screenshot of the Power BI dashboard here:
![Dashboard Preview](resources/dashboard-screenshot.png)
-->

![WhatsApp Image 2026-03-23 at 22 58 45](https://github.com/user-attachments/assets/937ce099-1172-4f63-9ea7-04d2b2db32ad)
![WhatsApp Image 2026-03-23 at 22 59 02](https://github.com/user-attachments/assets/10871af4-950f-4760-b95f-1b75857857df)
![WhatsApp Image 2026-03-23 at 22 59 29](https://github.com/user-attachments/assets/abbac2c5-65fc-494b-9d62-1e150cd9e740)


## Prerequisites

- **Lakehouse stack running** -- Trino must be accessible at `localhost:8080` (see [Lakehouse-Composes](../Lakehouse-Composes/))
- **Data loaded** -- At least one full run of both the CheapShark and Steam DAGs must have completed
- **Power BI Desktop** -- Required to open the `.pbix` file ([download](https://powerbi.microsoft.com/desktop/))

## Files

| File | Description |
|---|---|
| `steam-deals-dashboard.pbix` | Power BI dashboard file |
| `resources/filter-icon.png` | Custom filter icon used in the dashboard UI |
