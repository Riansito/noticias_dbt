SELECT

    api_news_id,
    COUNT(*) AS total

FROM {{ ref('fact_news') }}

GROUP BY api_news_id

HAVING COUNT(*) > 1