select "gameid", "title", "normalprice", "saleprice", "savings", "dealRating"
from {{ source('iceberg', 'cheapshark_data') }}