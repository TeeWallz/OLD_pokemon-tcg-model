
SELECT
    distinct series
FROM
    FROM {{ ref('vw_set') }}