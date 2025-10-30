-- back compat for old kwarg name
  
  
        
            
	    
	    
            
        
    

    

    merge into `desafio-civitas-brt-ari`.`brt_data`.`dbt_snapshots` as DBT_INTERNAL_DEST
        using (
        select
        * from `desafio-civitas-brt-ari`.`brt_data`.`dbt_snapshots__dbt_tmp`
        ) as DBT_INTERNAL_SOURCE
        on ((DBT_INTERNAL_SOURCE.unique_id = DBT_INTERNAL_DEST.unique_id))

    
    when matched then update set
        `unique_id` = DBT_INTERNAL_SOURCE.`unique_id`,`alias` = DBT_INTERNAL_SOURCE.`alias`,`checksum` = DBT_INTERNAL_SOURCE.`checksum`,`materialization` = DBT_INTERNAL_SOURCE.`materialization`,`tags` = DBT_INTERNAL_SOURCE.`tags`,`meta` = DBT_INTERNAL_SOURCE.`meta`,`owner` = DBT_INTERNAL_SOURCE.`owner`,`database_name` = DBT_INTERNAL_SOURCE.`database_name`,`schema_name` = DBT_INTERNAL_SOURCE.`schema_name`,`depends_on_macros` = DBT_INTERNAL_SOURCE.`depends_on_macros`,`depends_on_nodes` = DBT_INTERNAL_SOURCE.`depends_on_nodes`,`description` = DBT_INTERNAL_SOURCE.`description`,`name` = DBT_INTERNAL_SOURCE.`name`,`package_name` = DBT_INTERNAL_SOURCE.`package_name`,`original_path` = DBT_INTERNAL_SOURCE.`original_path`,`path` = DBT_INTERNAL_SOURCE.`path`,`patch_path` = DBT_INTERNAL_SOURCE.`patch_path`,`generated_at` = DBT_INTERNAL_SOURCE.`generated_at`,`metadata_hash` = DBT_INTERNAL_SOURCE.`metadata_hash`,`unique_key` = DBT_INTERNAL_SOURCE.`unique_key`,`incremental_strategy` = DBT_INTERNAL_SOURCE.`incremental_strategy`,`group_name` = DBT_INTERNAL_SOURCE.`group_name`,`access` = DBT_INTERNAL_SOURCE.`access`,`bigquery_partition_by` = DBT_INTERNAL_SOURCE.`bigquery_partition_by`,`bigquery_cluster_by` = DBT_INTERNAL_SOURCE.`bigquery_cluster_by`
    

    when not matched then insert
        (`unique_id`, `alias`, `checksum`, `materialization`, `tags`, `meta`, `owner`, `database_name`, `schema_name`, `depends_on_macros`, `depends_on_nodes`, `description`, `name`, `package_name`, `original_path`, `path`, `patch_path`, `generated_at`, `metadata_hash`, `unique_key`, `incremental_strategy`, `group_name`, `access`, `bigquery_partition_by`, `bigquery_cluster_by`)
    values
        (`unique_id`, `alias`, `checksum`, `materialization`, `tags`, `meta`, `owner`, `database_name`, `schema_name`, `depends_on_macros`, `depends_on_nodes`, `description`, `name`, `package_name`, `original_path`, `path`, `patch_path`, `generated_at`, `metadata_hash`, `unique_key`, `incremental_strategy`, `group_name`, `access`, `bigquery_partition_by`, `bigquery_cluster_by`)


    