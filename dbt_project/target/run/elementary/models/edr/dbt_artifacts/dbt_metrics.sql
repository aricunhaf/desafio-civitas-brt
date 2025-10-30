-- back compat for old kwarg name
  
  
        
            
	    
	    
            
        
    

    

    merge into `desafio-civitas-brt-ari`.`brt_data`.`dbt_metrics` as DBT_INTERNAL_DEST
        using (
        select
        * from `desafio-civitas-brt-ari`.`brt_data`.`dbt_metrics__dbt_tmp`
        ) as DBT_INTERNAL_SOURCE
        on ((DBT_INTERNAL_SOURCE.unique_id = DBT_INTERNAL_DEST.unique_id))

    
    when matched then update set
        `unique_id` = DBT_INTERNAL_SOURCE.`unique_id`,`name` = DBT_INTERNAL_SOURCE.`name`,`label` = DBT_INTERNAL_SOURCE.`label`,`model` = DBT_INTERNAL_SOURCE.`model`,`type` = DBT_INTERNAL_SOURCE.`type`,`sql` = DBT_INTERNAL_SOURCE.`sql`,`timestamp` = DBT_INTERNAL_SOURCE.`timestamp`,`filters` = DBT_INTERNAL_SOURCE.`filters`,`time_grains` = DBT_INTERNAL_SOURCE.`time_grains`,`dimensions` = DBT_INTERNAL_SOURCE.`dimensions`,`depends_on_macros` = DBT_INTERNAL_SOURCE.`depends_on_macros`,`depends_on_nodes` = DBT_INTERNAL_SOURCE.`depends_on_nodes`,`description` = DBT_INTERNAL_SOURCE.`description`,`tags` = DBT_INTERNAL_SOURCE.`tags`,`meta` = DBT_INTERNAL_SOURCE.`meta`,`package_name` = DBT_INTERNAL_SOURCE.`package_name`,`original_path` = DBT_INTERNAL_SOURCE.`original_path`,`path` = DBT_INTERNAL_SOURCE.`path`,`generated_at` = DBT_INTERNAL_SOURCE.`generated_at`,`metadata_hash` = DBT_INTERNAL_SOURCE.`metadata_hash`,`group_name` = DBT_INTERNAL_SOURCE.`group_name`
    

    when not matched then insert
        (`unique_id`, `name`, `label`, `model`, `type`, `sql`, `timestamp`, `filters`, `time_grains`, `dimensions`, `depends_on_macros`, `depends_on_nodes`, `description`, `tags`, `meta`, `package_name`, `original_path`, `path`, `generated_at`, `metadata_hash`, `group_name`)
    values
        (`unique_id`, `name`, `label`, `model`, `type`, `sql`, `timestamp`, `filters`, `time_grains`, `dimensions`, `depends_on_macros`, `depends_on_nodes`, `description`, `tags`, `meta`, `package_name`, `original_path`, `path`, `generated_at`, `metadata_hash`, `group_name`)


    