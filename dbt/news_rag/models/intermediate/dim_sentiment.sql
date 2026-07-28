WITH sentiment_data AS (

    SELECT DISTINCT

        sentiment -> 'body' ->> 'polarity' AS body_polarity,

        (sentiment -> 'body' ->> 'score')::NUMERIC AS body_score,

        sentiment -> 'title' ->> 'polarity' AS title_polarity,

        (sentiment -> 'title' ->> 'score')::NUMERIC AS title_score,

        sentiment -> 'overall' ->> 'polarity' AS overall_polarity,

        (sentiment -> 'overall' ->> 'score')::NUMERIC AS overall_score

    FROM {{ ref('stg_news') }}

)

SELECT

    {{ dbt_utils.generate_surrogate_key([
        'body_polarity',
        'body_score',
        'title_polarity',
        'title_score',
        'overall_polarity',
        'overall_score'
    ]) }} AS sentiment_key,

    *

FROM sentiment_data