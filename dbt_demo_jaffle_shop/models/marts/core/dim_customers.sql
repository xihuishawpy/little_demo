with customers as (

    select * from {{ ref('stg_customers') }}

),

orders as (

    select * from {{ ref('customer_orders') }}

),

payments as (

    select * from {{ ref('customer_payments') }}

),

final as (

    select
        customers.customer_id,
        orders.first_order,
        orders.most_recent_order,
        orders.number_of_orders,
        payments.total_amount as customer_lifetime_value

    from customers
    left join orders on customers.customer_id= orders.customer_id
    left join payments on  customers.customer_id = payments.customer_id

)

select * from final