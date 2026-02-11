with source as (
    select * from {{ source('steam', 'steam_data') }}
),

renamed as (
    select
        -- ids
        steam_appid as steam_app_id,

        -- strings
        "type" as "type",
        "name" as "name",
        controller_support as controller_support,
        detailed_description as detailed_description,
        about_the_game as about_the_game,
        short_description as short_description,
        supported_languages as supported_languages,
        header_image as header_image,
        website as website,
        legal_notice as legal_notice,
        background as background,

        -- numeric
        required_age as required_age,

        -- booleans
        is_free as is_free,

        -- dates

        -- arrays & structs
        dlc as dlc,
        fullgame as full_game,
        pc_requirements as pc_requirements,
        mac_requirements as mac_requirements,
        linux_requirements as linux_requirements,
        developers as developers,
        publishers as publishers,
        demos as demos,
        price_overview as price_overview,
        packages as packages,
        package_groups as package_groups,
        platforms as platforms,
        metacritic as metacritic,
        categories as categories,
        genres as genres,
        screenshots as screenshots,
        movies as movies,
        recommendations as recommendations,
        achievements as achievements,
        release_date as release_date,
        support_info as support_info,
        content_descriptors as content_descriptors

    from source
)

select *
from renamed