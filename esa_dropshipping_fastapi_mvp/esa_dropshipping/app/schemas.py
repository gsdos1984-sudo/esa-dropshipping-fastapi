from pydantic import BaseModel, EmailStr
from typing import List, Optional
from .models import OrderStatus

class ProductCreate(BaseModel):
    sku: str
    name: str
    description: Optional[str] = ""
    price_usd: float
    weight_kg: float = 0.0
    origin: str = "US"

class ProductOut(ProductCreate):
    id: int
    class Config:
        from_attributes = True

class OrderItemIn(BaseModel):
    product_id: int
    qty: int = 1

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    ship_to_city: str
    ship_to_state: str
    ship_to_zip: str
    items: List[OrderItemIn]

class OrderOut(BaseModel):
    id: int
    customer_name: str
    customer_email: EmailStr
    ship_to_city: str
    ship_to_state: str
    ship_to_zip: str
    status: OrderStatus
    class Config:
        from_attributes = True

class ShipmentCreate(BaseModel):
    order_id: int
    carrier: str = "DeliverFever"
    tracking: str = ""
    dest_city: str
    dest_state: str

class ShipmentOut(BaseModel):
    id: int
    order_id: int
    carrier: str
    tracking: str
    status: str
    origin_city: str
    origin_state: str
    dest_city: str
    dest_state: str
    class Config:
        from_attributes = True
