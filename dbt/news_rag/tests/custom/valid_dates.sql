SELECT *

FROM {{ ref('fact_news') }}

WHERE published_at > CURRENT_TIMESTAMP