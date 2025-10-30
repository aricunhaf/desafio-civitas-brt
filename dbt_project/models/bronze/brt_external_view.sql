{{ config(materialized='view', alias='brt_external_view') }}

select * from `desafio-civitas-brt-ari.brt_data.external_brt_data`