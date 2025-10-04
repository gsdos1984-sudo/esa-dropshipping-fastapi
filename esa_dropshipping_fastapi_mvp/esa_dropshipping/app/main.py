from fastapi import FastAPI
from .database import Base, engine
from .routers import products, orders, shipping

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ESA Dropshipping – Backend MVP")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(shipping.router)
