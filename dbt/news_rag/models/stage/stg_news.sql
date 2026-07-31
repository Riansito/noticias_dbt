{{
    config(
        materialized='incremental',
        unique_key='news_id'
    )
}}
WITH ranked_news AS (

    SELECT

        -------------------------------------------------------------------------
        -- Identificação
        -------------------------------------------------------------------------

        news_id,

        (payload ->> 'id')::BIGINT AS api_news_id,


        -------------------------------------------------------------------------
        -- Conteúdo
        -------------------------------------------------------------------------

        payload ->> 'title' AS title,

        payload ->> 'description' AS description,

        payload ->> 'text' AS body,


        -------------------------------------------------------------------------
        -- URLs
        -------------------------------------------------------------------------

        CASE
            WHEN payload ->> 'href' LIKE '//%' THEN
                'https:' || (payload ->> 'href')
            ELSE
                payload ->> 'href'
        END AS article_url,

        CASE
            WHEN payload ->> 'image' LIKE '//%' THEN
                'https:' || (payload ->> 'image')
            ELSE
                payload ->> 'image'
        END AS image_url,


        -------------------------------------------------------------------------
        -- Datas
        -------------------------------------------------------------------------

        (payload ->> 'published_at')::timestamp AS published_at,

        ingested_at,


        -------------------------------------------------------------------------
        -- Idioma
        -------------------------------------------------------------------------

        payload ->> 'language' AS language,


        -------------------------------------------------------------------------
        -- Objetos
        -------------------------------------------------------------------------

        payload -> 'author' AS author,

        payload -> 'source' AS source,

        payload -> 'sentiment' AS sentiment,


        -------------------------------------------------------------------------
        -- Arrays
        -------------------------------------------------------------------------

        payload -> 'categories' AS categories,

        payload -> 'topics' AS topics,

        payload -> 'industries' AS industries,

        payload -> 'entities' AS entities,

        payload -> 'keywords' AS keywords,


        -------------------------------------------------------------------------
        -- IA
        -------------------------------------------------------------------------

        payload ->> 'summary' AS summary,


        ROW_NUMBER() OVER (

            PARTITION BY
                (payload ->> 'id')::BIGINT

            ORDER BY
                ingested_at DESC

        ) AS rn


    FROM {{ source('raw', 'news') }}
{% if is_incremental() %}

WHERE ingested_at >
(
    SELECT COALESCE(MAX(ingested_at), '1900-01-01')
    FROM {{ this }}
)

{% endif %}
)


SELECT

    news_id,
    api_news_id,
    title,
    description,
    body,
    article_url,
    image_url,
    published_at,
    ingested_at,
    language,
    author,
    source,
    sentiment,
    categories,
    topics,
    industries,
    entities,
    keywords,
    summary

FROM ranked_news

WHERE rn = 1