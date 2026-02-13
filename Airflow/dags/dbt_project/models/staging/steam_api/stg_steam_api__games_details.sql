with source as (
    select * from {{ source('steam', 'steam_data') }}
),

renamed as (
    select
        --- id ---
        CAST(steam_appid AS VARCHAR) as steam_app_id,

        --- strings ---
        "type" as "type",
        "name" as "name",
        -- controller_support as controller_support,
        -- detailed_description as detailed_description,
        -- about_the_game as about_the_game,
        short_description as short_description,
        supported_languages as supported_languages,
        header_image as header_image,
        website as website,
        legal_notice as legal_notice,
        -- background as background,
        metacritic.url as metacritic_url,

        --- numeric ---
        required_age as required_age,
        price_overview.currency as price_currency,
        price_overview.initial as initial_price,
        price_overview.final as final_price,
        price_overview.discount_percent as discount_percent,
        price_overview.initial_formatted as initial_price_formatted,
        price_overview.final_formatted as final_price_formatted,
        recommendations.total as total_recommendations,
        metacritic.score as metacritic_score,

        --- booleans ---
        case when controller_support = 'full' then true else false end as is_support_controller,
        is_free as is_free,
        platforms.windows as is_available_on_windows,
        platforms.mac as is_available_on_mac,
        platforms.linux as is_available_on_linux,
        release_date.coming_soon as is_coming_soon,

        --- dates ---
        CAST(date_parse(release_date.date, '%d %M, %Y') as date) as release_date,

        --- arrays & structs ---
        -- dlc as dlc,
        -- fullgame as full_game,
        -- pc_requirements as pc_requirements,
        -- mac_requirements as mac_requirements,
        -- linux_requirements as linux_requirements,
        developers as developers,
        publishers as publishers,
        -- demos as demos,
        -- price_overview as price_overview,
        -- packages as packages,
        -- package_groups as package_groups,
        -- platforms as platforms,
        -- metacritic as metacritic,
        categories as categories,
        genres as genres
        -- screenshots as screenshots,
        -- movies as movies,
        -- recommendations as recommendations,
        -- achievements as achievements,
        -- release_date as release_date,
        -- support_info as support_info,
        -- content_descriptors as content_descriptors

    from source
)

select *
from renamed