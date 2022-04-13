
    
    




with all_values as (

    select distinct
        payment_method as value_field

    from lcj.stg_payments

),

validation_errors as (

    select
        value_field

    from all_values
    where value_field not in (
        'credit_card','coupon','bank_transfer','gift_card'
    )
)

select count(*)
from validation_errors


