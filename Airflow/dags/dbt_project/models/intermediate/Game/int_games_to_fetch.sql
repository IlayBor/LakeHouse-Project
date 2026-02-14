{{ config(materialized='table') }}

select distinct cheapshark_deals.steam_app_id from {{ ref("stg_cheapshark_api__game_deals") }} cheapshark_deals
except
select distinct steam_app_id from {{ ref( "stg_steam_api__games_details" ) }}