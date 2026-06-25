WITH steam_games as (
    select *
    from {{ ref("stg_steam_api__games_details") }}
),

game_genres as (
    select steam_app_id, genre_id, genre_desc
    from steam_games
    cross join unnest(genres) as t(genre_id, genre_desc)
)

select * 
from game_genres