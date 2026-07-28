WITH industry_data AS (

    SELECT

        jsonb_array_elements(industries) AS industry

    FROM {{ ref('stg_news') }}

),

industry_clean AS (

    SELECT DISTINCT

        (industry ->> 'id')::BIGINT AS industry_id,

        industry ->> 'name' AS industry_name,

        industry -> 'links' ->> 'self' AS self_link

    FROM industry_data

)

SELECT

    {{ dbt_utils.generate_surrogate_key(['industry_id']) }} AS industry_key,

    industry_id,

    industry_name,

    self_link

FROM industry_clean