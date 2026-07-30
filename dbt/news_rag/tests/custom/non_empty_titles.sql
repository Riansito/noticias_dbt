SELECT *

FROM {{ ref('fact_news') }}

WHERE title IS NULL

OR trim(title) = ''