WITH source_data AS (

    SELECT DISTINCT

        source ->> 'id' AS source_id,

        source ->> 'bias' AS bias,

        source ->> 'type' AS source_type,

        source ->> 'domain' AS domain,

        source ->> 'favicon' AS favicon,

        source ->> 'home_page_url' AS home_page_url,

        source -> 'location' ->> 'country_code' AS country_code,

        source -> 'location' ->> 'country_name' AS country_name,

        (source -> 'rankings' ->> 'opr')::INTEGER AS opr_rank

    FROM {{ ref('stg_news') }}

    WHERE source IS NOT NULL

)

SELECT

    {{ dbt_utils.generate_surrogate_key(['source_id']) }} AS source_key,

    *

FROM source_data