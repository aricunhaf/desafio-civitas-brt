

  create or replace view `desafio-civitas-brt-ari`.`brt_data`.`consolidated_brt_data`
  OPTIONS(
      description="""Camada Silver - Dados limpos e normalizados do BRT."""
    )
  as 

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
from `desafio-civitas-brt-ari`.`brt_data`.`brt_external_view`
where latitude is not null 
  and longitude is not null;

