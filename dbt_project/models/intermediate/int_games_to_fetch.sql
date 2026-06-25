{{ config(materialized='table') }}
-- depends_on: {{ ref('stg_steam_api__games_details') }}

{%- set relation = adapter.get_relation(
    database="iceberg",
    schema="staging",
    identifier="stg_steam_api__games_details") %}

select distinct cheapshark_deals.steam_app_id from {{ ref("stg_cheapshark_api__game_deals") }} cheapshark_deals
{%- if relation is not none %}
except
select distinct steam_app_id from {{ ref("stg_steam_api__games_details") }}
{% endif %}
