from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..config import settings

router = APIRouter(prefix="/shipping", tags=["shipping"]) 

@router.post("/create", response_model=schemas.ShipmentOut)
def create_shipment(payload: schemas.ShipmentCreate, db: Session = Depends(get_db)):
    order = db.query(models.Order).get(payload.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    shipment = models.Shipment(
        order_id=order.id,
        carrier=payload.carrier,
        tracking=payload.tracking or "PENDING-TRACKING",
        status="label_created",
        origin_city=settings.DF_CITY,
        origin_state=settings.DF_STATE,
        dest_city=payload.dest_city,
        dest_state=payload.dest_state,
    )
    db.add(shipment)

    # Cambiar estado del pedido a "forwarding"
    order.status = models.OrderStatus.forwarding

    db.commit()
    db.refresh(shipment)
    return shipment

@router.post("/{shipment_id}/status/{new_status}")
def update_shipment_status(shipment_id: int, new_status: str, db: Session = Depends(get_db)):
    shp = db.query(models.Shipment).get(shipment_id)
    if not shp:
        raise HTTPException(status_code=404, detail="Shipment not found")
    shp.status = new_status

    # Propagar al pedido si aplica
    order = db.query(models.Order).get(shp.order_id)
    if new_status == "at_df":
        order.status = models.OrderStatus.at_df
    elif new_status == "in_transit_mx":
        order.status = models.OrderStatus.in_transit_mx
    elif new_status == "delivered":
        order.status = models.OrderStatus.delivered

    db.commit()
    return {"ok": True, "shipment_id": shipment_id, "status": new_status}
@router.get("/")
def list_shipments(db: Session = Depends(get_db)):
    return db.query(models.Shipment).all()
