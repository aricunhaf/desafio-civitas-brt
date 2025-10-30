{{ config(
    materialized='view'
) }}

select
  cast(codigo as string) as codigo,
  cast(linha as string) as linha,
  latitude,
  longitude,
  timestamp_millis(dataHora) as data_hora,
  velocidade,
  trajeto,
  sentido,
  captured_at
from {{ ref('brt_external_view') }}
where latitude is not null 
  and longitude is not null