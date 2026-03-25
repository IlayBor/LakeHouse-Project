select 
	cheapshark."deal_id", 
	cheapshark."deal_rating",
	cheapshark."steam_app_id",
	cheapshark."steam_rating_percent",
	cheapshark."steam_rating_count",
	cheapshark."normal_price",
	cheapshark."sale_price",
	cheapshark."discount_percent",
	steam_details."name",
	steam_details."short_description",
	steam_details."header_image",
	steam_details."website",
	steam_details."required_age",
	steam_details."total_recommendations",
	steam_details."metacritic_score",
	steam_details."is_support_controller",
	steam_details."is_available_on_windows",
	steam_details."is_available_on_mac",
	steam_details."is_available_on_linux",
	steam_details."release_date",
	cheapshark."ingestion_date"
from {{ ref("stg_cheapshark_api__game_deals") }} cheapshark 
inner join {{ ref("stg_steam_api__games_details") }} steam_details on (cheapshark."steam_app_id" = steam_details."steam_app_id")