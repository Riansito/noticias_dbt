WITH topic_data AS (

    SELECT

        jsonb_array_elements(topics) AS topic

    FROM {{ ref('stg_news') }}

),

topic_clean AS (

    SELECT DISTINCT

        topic ->> 'id' AS topic_id,

        topic ->> 'name' AS topic_name,

        topic -> 'links' ->> 'self' AS self_link

    FROM topic_data

)

SELECT

    {{ dbt_utils.generate_surrogate_key(['topic_id']) }} AS topic_key,

    topic_id,

    topic_name,

    self_link

FROM topic_clean