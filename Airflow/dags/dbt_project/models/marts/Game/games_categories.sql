WITH steam_games as (
    select *
    from {{ ref("stg_steam_api__games_details") }}
),

game_categories as (
    select steam_app_id, category_id, category_desc
    from steam_games
    cross join unnest(categories) as t(category_id, category_desc)
)

select * 
from game_categories