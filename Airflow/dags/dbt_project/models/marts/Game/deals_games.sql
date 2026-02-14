select 
	cheapshark.ingestion_date, 
	cheapshark.deal_id, 
	cheapshark.steam_app_id, 
	steam.name,
	steam.short_description,
	steam.header_image,
	steam.required_age, 
	steam.is_support_controller,
	steam.is_available_on_windows ,
	steam.is_available_on_mac,
	steam.is_available_on_linux,
	steam.release_date,
	cheapshark.sale_price, 
	cheapshark.normal_price, 
	cheapshark.discount_percent, 
	cheapshark.steam_rating_percent,
	cheapshark.steam_rating_count , 
	cheapshark.deal_rating
from {{ ref("stg_cheapshark_api__game_deals") }} cheapshark
inner join {{ ref("stg_steam_api__games_details") }} steam on (cheapshark.steam_app_id = steam.steam_app_id)