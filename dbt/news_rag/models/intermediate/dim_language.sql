WITH language_data AS (

    SELECT DISTINCT

        language

    FROM {{ ref('stg_news') }}

    WHERE language IS NOT NULL

)

SELECT

    {{ dbt_utils.generate_surrogate_key(['language']) }} AS language_key,
    COALESCE(language, 'Unknown') AS language

FROM language_data