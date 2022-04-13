
  create view lcj.stg_customers__dbt_tmp as
    with source as (
    select * from lcj.raw_customers

),

renamed as (

    select
        id as customer_id,
        first_name,
        last_name

    from source

)

select * from renamed

