from unit_of_work.models import Order, OrderItem


order_data = {
    'user_id': 'd1e20a44-b5cf-4d34-b9cd-4ee3d6c23f59',
    'order_items': [
        {
            'product_id': '179d74ab-d2cd-4eef-a6c0-526d5c1606cc',
            'quantity': 4
        },
        {
            'product_id': '3dc761d2-a3db-4672-a1a9-e002635afe70',
            'quantity': 5
        }
    ]
}


def create_order_traditional(data):
    user_id = data.pop('user_id')
    order = Order(user_id=user_id)
    session.add(order)
    session.commit()
    for item in data['order_items']:
        order_item = OrderItem(order_id=order.id, product_id=item['product_id'], quantity=item['quantity'])
        session.add(order_item)
        session.commit()


def create_order_unit_of_work(data):
    user_id = data.pop('user_id')
    order_item_object_list = []
    for item in data['order_items']:
        order_item = OrderItem(product_id=item['product_id'], quantity=item['quantity'])
        order_item_object_list.append(order_item)
    order = Order(user_id=user_id, order_items=order_item_object_list)
    session.add(order)
    session.commit()
