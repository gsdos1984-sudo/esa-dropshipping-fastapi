from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=schemas.OrderOut)
def create_order(payload: schemas.OrderCreate, db: Session = Depends(get_db)):
    # validar productos
    for it in payload.items:
        prod = db.query(models.Product).get(it.product_id)
        if not prod:
            raise HTTPException(status_code=404, detail=f"Product {it.product_id} not found")

    order = models.Order(
        customer_name=payload.customer_name,
        customer_email=payload.customer_email,
        ship_to_city=payload.ship_to_city,
        ship_to_state=payload.ship_to_state,
        ship_to_zip=payload.ship_to_zip,
    )
    db.add(order)
    db.flush()
@router.get("/", response_model=list[schemas.OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

    for it in payload.items:
        db.add(models.OrderItem(order_id=order.id, product_id=it.product_id, qty=it.qty))

    db.commit()
    db.refresh(order)
    return order

@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
@router.get("/", response_model=list[schemas.OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()
