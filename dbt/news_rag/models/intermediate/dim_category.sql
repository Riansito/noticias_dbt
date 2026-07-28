WITH category_data AS (

    SELECT

        jsonb_array_elements(categories) AS category

    FROM {{ ref('stg_news') }}

),

category_clean AS (

    SELECT DISTINCT

        (category ->> 'id')::BIGINT AS category_id,

        category ->> 'name' AS category_name,

        category ->> 'taxonomy' AS taxonomy,

        category -> 'links' ->> 'self' AS self_link

    FROM category_data

)

SELECT

    {{ dbt_utils.generate_surrogate_key(['category_id']) }} AS category_key,

    category_id,

    category_name,

    taxonomy,

    self_link

FROM category_clean