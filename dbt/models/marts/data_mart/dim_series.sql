
SELECT
    distinct series
FROM
    {{ ref('vw_set') }}