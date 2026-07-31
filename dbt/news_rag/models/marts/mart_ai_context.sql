WITH categories AS (

    SELECT

        b.news_key,

        STRING_AGG(
            c.category_name,
            ', '
            ORDER BY c.category_name
        ) AS categories

    FROM {{ ref('bridge_news_category') }} b

    JOIN {{ ref('dim_category') }} c
        ON b.category_key = c.category_key

    GROUP BY b.news_key

),

topics AS (

    SELECT

        b.news_key,

        STRING_AGG(
            t.topic_name,
            ', '
            ORDER BY t.topic_name
        ) AS topics

    FROM {{ ref('bridge_news_topic') }} b

    JOIN {{ ref('dim_topic') }} t
        ON b.topic_key = t.topic_key

    GROUP BY b.news_key

),

industries AS (

    SELECT

        b.news_key,

        STRING_AGG(
            i.industry_name,
            ', '
            ORDER BY i.industry_name
        ) AS industries

    FROM {{ ref('bridge_news_industry') }} b

    JOIN {{ ref('dim_industry') }} i
        ON b.industry_key = i.industry_key

    GROUP BY b.news_key

)

SELECT

    f.news_key,

    f.news_id,

    ----------------------------------------------------
    -- Conteúdo
    ----------------------------------------------------

    f.title,

    f.description,

    f.summary,

    ----------------------------------------------------
    -- Fonte
    ----------------------------------------------------

    s.domain ,
    s.country_name,

    ----------------------------------------------------
    -- Autor
    ----------------------------------------------------

    a.author_name,

    ----------------------------------------------------
    -- Sentimento
    ----------------------------------------------------

    se.overall_polarity,

    se.overall_score,

    ----------------------------------------------------
    -- Classificações
    ----------------------------------------------------

    c.categories,

    t.topics,

    i.industries,

    ----------------------------------------------------
    -- Links
    ----------------------------------------------------

    f.article_url,

    f.image_url,

    ----------------------------------------------------
    -- Datas
    ----------------------------------------------------

    f.published_at,

    f.ingested_at,

    CONCAT_WS(

        E'\n\n',

        'Title: ' || COALESCE(f.title,''),

        'Description: ' || COALESCE(f.description,''),

        'Summary: ' || COALESCE(f.summary,''),

        'Author: ' || COALESCE(a.author_name,''),

        'Source: ' || COALESCE(s.domain,''),

        'Country: ' || COALESCE(s.country_name,''),

        'Categories: ' || COALESCE(c.categories,''),

        'Topics: ' || COALESCE(t.topics,''),

        'Industries: ' || COALESCE(i.industries,''),

        'Sentiment: '
        || COALESCE(se.overall_polarity,'')
        || ' ('
        || COALESCE(se.overall_score::text,'')
        || ')'

    ) AS context

FROM {{ ref('fact_news') }} f

LEFT JOIN {{ ref('dim_source') }} s
ON f.source_key = s.source_key

LEFT JOIN {{ ref('dim_author') }} a
ON f.author_key = a.author_key

LEFT JOIN {{ ref('dim_sentiment') }} se
ON f.sentiment_key = se.sentiment_key

LEFT JOIN categories c
ON f.news_key = c.news_key

LEFT JOIN topics t
ON f.news_key = t.news_key

LEFT JOIN industries i
ON f.news_key = i.news_key