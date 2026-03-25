WITH steam_games as (
    select *
    from {{ ref("stg_steam_api__games_details") }}
),

game_developers as (
    select steam_app_id, developer_id
    from steam_games
    cross join unnest(developers) as t(developer_id)
)

select * 
from game_developers