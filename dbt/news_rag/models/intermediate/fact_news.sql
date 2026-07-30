WITH source_lookup AS (

    SELECT *

    FROM {{ ref('dim_source') }}

),

author_lookup AS (

    SELECT *

    FROM {{ ref('dim_author') }}

),

sentiment_lookup AS (

    SELECT *

    FROM {{ ref('dim_sentiment') }}

)

SELECT

    ----------------------------------------------------
    -- Keys
    ----------------------------------------------------

    {{ dbt_utils.generate_surrogate_key(['news_id']) }} AS news_key,

    news_id,

    s.source_key,

    a.author_key,

    se.sentiment_key,

    ----------------------------------------------------
    -- Content
    ----------------------------------------------------

    title,

    description,

    summary,

    article_url,

    image_url,

    ----------------------------------------------------
    -- Metadata
    ----------------------------------------------------

    language,

    published_at,

    ingested_at,

    CURRENT_TIMESTAMP AS created_at

FROM {{ ref('stg_news') }} stg

LEFT JOIN source_lookup s
ON (stg.source ->> 'id') = s.source_id

LEFT JOIN author_lookup a
ON (stg.author ->> 'id') = a.author_id

LEFT JOIN sentiment_lookup se
ON
    (stg.sentiment -> 'body' ->> 'polarity') = se.body_polarity
AND (stg.sentiment -> 'body' ->> 'score')::NUMERIC = se.body_score
AND (stg.sentiment -> 'title' ->> 'polarity') = se.title_polarity
AND (stg.sentiment -> 'title' ->> 'score')::NUMERIC = se.title_score
AND (stg.sentiment -> 'overall' ->> 'polarity') = se.overall_polarity
AND (stg.sentiment -> 'overall' ->> 'score')::NUMERIC = se.overall_score