from sqlalchemy import String, Integer, Float, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
import enum

class OrderStatus(str, enum.Enum):
    pending = "pending"
    purchasing = "purchasing"          # orden colocada al proveedor
    at_df = "at_df"                    # recibido en Deliver Fever
    forwarding = "forwarding"          # reenviándose a MX
    in_transit_mx = "in_transit_mx"    # transporte en México
    delivered = "delivered"

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1000), default="")
    price_usd: Mapped[float] = mapped_column(Float)
    weight_kg: Mapped[float] = mapped_column(Float, default=0.0)
    origin: Mapped[str] = mapped_column(String(32), default="US")

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_name: Mapped[str] = mapped_column(String(255))
    customer_email: Mapped[str] = mapped_column(String(255))
    ship_to_city: Mapped[str] = mapped_column(String(100))
    ship_to_state: Mapped[str] = mapped_column(String(100))
    ship_to_zip: Mapped[str] = mapped_column(String(20))
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.pending)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    qty: Mapped[int] = mapped_column(Integer, default=1)

    order = relationship("Order", backref="items")
    product = relationship("Product")

class Shipment(Base):
    __tablename__ = "shipments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    carrier: Mapped[str] = mapped_column(String(64), default="DeliverFever")
    tracking: Mapped[str] = mapped_column(String(128), default="")
    status: Mapped[str] = mapped_column(String(64), default="label_created")
    origin_city: Mapped[str] = mapped_column(String(64))
    origin_state: Mapped[str] = mapped_column(String(16))
    dest_city: Mapped[str] = mapped_column(String(64))
    dest_state: Mapped[str] = mapped_column(String(16))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order")
