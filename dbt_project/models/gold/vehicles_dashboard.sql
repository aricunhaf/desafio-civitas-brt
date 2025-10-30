{{ config(
    materialized='view'
) }}

select
  linha,
  sentido,
  count(distinct codigo) as total_veiculos,
  round(avg(velocidade), 2) as velocidade_media,
  max(data_hora) as ultima_atualizacao
from {{ ref('consolidated_brt_data') }}   -- 👈 referência à Silver
group by linha, sentido
order by linha, sentido