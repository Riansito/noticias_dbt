WITH news_category AS (

    SELECT

        {{ dbt_utils.generate_surrogate_key(['news_id']) }} AS news_key,

        jsonb_array_elements(categories) AS category

    FROM {{ ref('stg_news') }}

),

category_lookup AS (

    SELECT *

    FROM {{ ref('dim_category') }}

)

SELECT

    nc.news_key,

    dc.category_key,

    (nc.category ->> 'score')::NUMERIC AS score

FROM news_category nc

INNER JOIN category_lookup dc

    ON (nc.category ->> 'id')::BIGINT = dc.category_id