DROP TABLE IF EXISTS categories,customer_customer_demo,customer_demographics,customers,employee_territories,employees,order_details,orders,products,region,shippers,suppliers,territories,us_states;

---

select
	o.order_id,
	c.company_name,
	c.country as company_country,
	p.product_name,
	p.quantity_per_unit,
	od.unit_price,
	od.quantity,
	od.discount,
	(od.unit_price * od.quantity) * (1 - od.discount) as final_price
from
	orders o
left join order_details od on
	od.order_id = o.order_id
	and od.extracted_at = o.extracted_at
inner join customers c on
	c.customer_id = o.customer_id
	and c.extracted_at = o.extracted_at
inner join products p on
	p.product_id = od.product_id
	and p.extracted_at = od.extracted_at 