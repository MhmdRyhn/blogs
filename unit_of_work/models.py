# Import all the necessary code from SQLAlchemy


class Order(Base):
    __tablename__ = 'order'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Foreign key referencing User model. User model is not shown here for simplicity
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete='RESTRICT'), nullable=False)
    last_updated_at = Column(DateTime, nullable=False, onupdate=func.utcnow, default=datetime.datetime.utcnow)
    # Related objects of an Order
    order_items = relationship('OrderItem', backref='order', uselist=True)


class OrderItem(Base):
    __tablename__ = 'orde_item'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("order.id", ondelete='RESTRICT'), nullable=False)
    # Foreign key referencing Product model. Product model is not shown here for simplicity
    product_id = Column(UUID(as_uuid=True), ForeignKey("product.id", ondelete='RESTRICT'), nullable=False)
    quantity = Column(Integer, nullable=False)
    last_updated_at = Column(DateTime, nullable=False, onupdate=func.utcnow, default=datetime.datetime.utcnow)
