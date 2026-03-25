WITH steam_games as (
    select *
    from {{ ref("stg_steam_api__games_details") }}
),

game_publishers as (
    select steam_app_id, publisher_id
    from steam_games
    cross join unnest(publishers) as t(publisher_id)
)

select * 
from game_publishers