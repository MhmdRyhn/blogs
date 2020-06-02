# SQLAlchemy and the Unit of Work Pattern
This blog post assumes that you are already familiar with SQLAlchemy, know how to setup and connect to database 
and how to play with basic operations using SQLAlchemy, an ORM written in Python for Relational Databases. 


## Traditional way to do a business transaction
When a business transaction involves several database operations, traditionally what you do is you perform each 
operation separately inside a transaction block. This can lead to lots of very small database calls, which ends 
up being very slow. Moreover it requires you to have a transaction open for the whole interaction, which is 
impractical if a business transaction needs multiple requests to be completed.

This is a problem in traditional way of performing a business transaction. The Unit of Work design pattern helps 
to solve these kind of situations.


## What is Unit of Work Pattern and How It Works
A Unit of work is a design pattern which is basically used in performing database transactions.

A Unit of Work is used to maintain a list of objects affected by a business transaction and to coordinate the 
writing out of these changes. - Martin Fowler

A Unit of Work keeps track of everything you do during a business transaction that can affect the database. When 
you're done, it figures out everything that needs to be done to alter the database as a result of your work [2]. 
Unit of Work design pattern does two important things [3]: 

(1) It maintains lists of business objects in-memory which have been changed (inserted, updated, or deleted) during 
a transaction.
(2) It then sends these in-memory updates as one big unit of work (transaction) to the database.

Still confusing? Lets illustrate this with an example.

### The Problem:
Suppose, you have an e-commerce application, where your users can order products by using your application. When 
a user creates an order, this order can contain several items of different quantity. You need to save the order 
along with the items and the quantity into the database.

Suppose the Database models are as follows:

**Note:** The models bellow are `PostgreSQL` compatible only. You can use any other Relational Databases 
supported by SQLAlchemy and change the models accordingly.

`models.py`
```
class Order(Base):
    __tablename__ = 'order'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Foreign key referencing User model. User model is not shown here for simplicity
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete='RESTRICT'), nullable=False)
    last_updated_at = Column(DateTime, nullable=False, onupdate=func.utcnow, default=datetime.datetime.utcnow)
    # Related items of an order
    order_items = relationship('OrderItem', backref='order', uselist=True)


class OrderItem(Base):
    __tablename__ = 'order_item'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("order.id", ondelete='RESTRICT'), nullable=False)
    # Foreign key referencing Product model. Product model is not shown here for simplicity
    product_id = Column(UUID(as_uuid=True), ForeignKey("product.id", ondelete='RESTRICT'), nullable=False)
    quantity = Column(Integer, nullable=False)
    last_updated_at = Column(DateTime, nullable=False, onupdate=func.utcnow, default=datetime.datetime.utcnow)
```

And, the incoming data having the order details is of the following structure:

```
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
```

### Solution 1: using the traditional way 

`operations.py`

```
def create_order_traditional(data):
    user_id = data.pop('user_id')
    order = Order(user_id=user_id)
    session.add(order)
    session.commit()
    for item in data['order_items']:
        order_item = OrderItem(order_id=order.id, product_id=item['product_id'], quantity=item['quantity'])
        session.add(order_item)
        session.commit()
    session.close()
```
In the above order creation operation, `session.commit()` will be called 3 times to complete the transaction, i.e., 
it's calling database 3 times. So, what if the payload you are saving is much bigger? This will use more number 
of database call. 

Let's try to get the same effect in database using Unit of Work.


### Solution 2: using Unit of Work Pattern

`operations.py`

```
def create_order_unit_of_work(data):
    user_id = data.pop('user_id')
    order_item_object_list = []
    for item in data['order_items']:
        order_item = OrderItem(product_id=item['product_id'], quantity=item['quantity'])
        order_item_object_list.append(order_item)
    order = Order(user_id=user_id, order_items=order_item_object_list)
    session.add(order)
    session.commit()
    session.close()
```

Here, notice that `session.commit()` is called only once. All the other operations (in this case, the insert) were done 
in-memory and then sent to database as a big unit of work. SQLAlchemy will handle the rest of the thing using Unit of 
Work pattern. This way is much more efficient than the traditional one. It doesn't require you to save each object 
separately, thus helps to prevent the transaction being slow. You just need to manipulate the objects in-memory and then 
send the whole unit of objects at a time, SQLAlchemy will handle the rest of the thing on your behalf. This pattern can 
be applied in the case of update and delete operations too. In those cases, you'll update / delete multiple objects 
in-memory and finally apply `session.commit()` to reflect the changes in database.

SQLAlchemy is a very powerful and easy to use ORM written in Python. It really helps to develop application faster.


## References
[1] [SQLAlchemy: Session / Unit of Work](https://docs.huihoo.com/python/sqlalchemy-0.3/unitofwork.html)

[2] [Unit of Work by Martin Fowler](https://martinfowler.com/eaaCatalog/unitOfWork.html)

[3] [Unit of Work Design Pattern](https://www.codeproject.com/Articles/581487/Unit-of-Work-Design-Pattern)

[4] [SQLAlchemy ORM Tutorial for Python Developer](https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers)
