WITH news_topic AS (

    SELECT

        {{ dbt_utils.generate_surrogate_key(['news_id']) }} AS news_key,

        jsonb_array_elements(topics) AS topic

    FROM {{ ref('stg_news') }}

),

topic_lookup AS (

    SELECT *

    FROM {{ ref('dim_topic') }}

)

SELECT

    nt.news_key,

    dt.topic_key,

    (nt.topic ->> 'score')::NUMERIC AS score

FROM news_topic nt

INNER JOIN topic_lookup dt

    ON nt.topic ->> 'id' = dt.topic_id