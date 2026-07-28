WITH news_industry AS (

    SELECT

        {{ dbt_utils.generate_surrogate_key(['news_id']) }} AS news_key,

        jsonb_array_elements(industries) AS industry

    FROM {{ ref('stg_news') }}

),

industry_lookup AS (

    SELECT *

    FROM {{ ref('dim_industry') }}

)

SELECT

    ni.news_key,

    di.industry_key

FROM news_industry ni

INNER JOIN industry_lookup di

    ON (ni.industry ->> 'id')::BIGINT = di.industry_id