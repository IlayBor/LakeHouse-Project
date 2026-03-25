with source as (
    select * from {{ source('cheapshark', 'cheapshark_data') }}
),

renamed as (
    select
        -- ids
        dealid as deal_id,
        storeid as store_id,
        gameid as game_id,
        CAST(steamappid AS VARCHAR) as steam_app_id,

        -- strings
        internalname as internal_name,
        title as title,
        metacriticlink as meta_critic_link,
        steamratingtext as steam_rating_text,
        thumb as thumb,

        -- numeric
        saleprice as sale_price,
        normalprice as normal_price,
        savings as discount_percent,
        metacriticscore as meta_critic_score,
        steamratingpercent as steam_rating_percent,
        steamratingcount as steam_rating_count,
        dealrating as deal_rating,

        -- booleans
        isonsale as is_on_sale,

        -- dates
        CAST(from_unixtime(releasedate) AS date) AS release_date,
        CAST(from_unixtime(lastchange) AS date) AS last_change_date,
        CAST(ingestiondate AS date) AS ingestion_date

    from source
)

select *
from renamed