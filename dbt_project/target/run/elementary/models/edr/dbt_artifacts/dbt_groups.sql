-- back compat for old kwarg name
  
  
        
            
	    
	    
            
        
    

    

    merge into `desafio-civitas-brt-ari`.`brt_data`.`dbt_groups` as DBT_INTERNAL_DEST
        using (
        select
        * from `desafio-civitas-brt-ari`.`brt_data`.`dbt_groups__dbt_tmp`
        ) as DBT_INTERNAL_SOURCE
        on ((DBT_INTERNAL_SOURCE.unique_id = DBT_INTERNAL_DEST.unique_id))

    
    when matched then update set
        `unique_id` = DBT_INTERNAL_SOURCE.`unique_id`,`name` = DBT_INTERNAL_SOURCE.`name`,`owner_email` = DBT_INTERNAL_SOURCE.`owner_email`,`owner_name` = DBT_INTERNAL_SOURCE.`owner_name`,`generated_at` = DBT_INTERNAL_SOURCE.`generated_at`,`metadata_hash` = DBT_INTERNAL_SOURCE.`metadata_hash`
    

    when not matched then insert
        (`unique_id`, `name`, `owner_email`, `owner_name`, `generated_at`, `metadata_hash`)
    values
        (`unique_id`, `name`, `owner_email`, `owner_name`, `generated_at`, `metadata_hash`)


    