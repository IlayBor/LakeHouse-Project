select "gameid", "title"
from {{ source('iceberg', 'fct_sales') }}