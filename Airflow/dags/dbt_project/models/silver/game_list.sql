select "gameid", "title"
from {{ ref('short_sales') }}