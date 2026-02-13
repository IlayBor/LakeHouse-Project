WITH steam_games as (
    select *
    from {{ ref("stg_steam_api__game_details") }}
),

pivot_game_categories as (
    select steam_app_id, category_id, category_desc
    from steam_games
    cross join unnest(categories) as t(category_id, category_desc)
)

select * 
from pivot_game_categories