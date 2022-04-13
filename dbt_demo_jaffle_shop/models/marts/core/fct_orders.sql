{% set payment_methods = ['credit_card', 'coupon', 'bank_transfer', 'gift_card'] %}

with orders as (

    select * from {{ ref('stg_orders') }}

),

payments as (

    select * from {{ ref('order_payments') }}

),

final as (

    select
        orders.order_id,
        orders.customer_id,
        orders.order_date,
        orders.status,

        {% for payment_method in payment_methods -%}

        payments.{{payment_method}}_amount,

        {% endfor -%}

        payments.total_amount as amount

    from orders

    left join payments on  orders.order_id = payments.order_id

)

select * from final
