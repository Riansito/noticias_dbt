SELECT

    article_url,
    COUNT(*) AS total

FROM {{ ref('fact_news') }}

WHERE article_url IS NOT NULL

GROUP BY article_url

HAVING COUNT(*) > 1