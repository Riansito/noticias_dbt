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

        payload ->> 'href' AS article_url,

        payload ->> 'image' AS image_url,


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