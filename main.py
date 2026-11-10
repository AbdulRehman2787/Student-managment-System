from fastapi import FastAPI
from database import engine, Base

from models.product import Product
from models.customer import Customer
from models.order import Order

from routers import product, customer, order

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shop Management API")

app.include_router(product.router)
app.include_router(customer.router)
app.include_router(order.router)

@app.get("/")
def home():
    return {"message": "Shop API is running"}