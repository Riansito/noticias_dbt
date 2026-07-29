WITH author_data AS (

    SELECT DISTINCT

        (author ->> 'id') AS author_id,

        NULLIF(TRIM(author ->> 'name'), '') AS author_name

    FROM {{ ref('stg_news') }}

    WHERE author IS NOT NULL

)

SELECT

    {{ dbt_utils.generate_surrogate_key(['author_id']) }} AS author_key,

    author_id,

    COALESCE(author_name, 'Unknown') AS author_name

FROM author_data