SELECT *

FROM {{ ref('fact_news') }}

WHERE article_url IS NOT NULL

AND article_url !~ '^https?://'