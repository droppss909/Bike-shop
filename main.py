from fastapi import FastAPI
from customers.router import router as customers_router
from bikes.router import router as bikes_router
from database.database import engine
from services.router import router as service_router
from orders.router import router as order_router
from bills.router import router as bill_router

app = FastAPI()

app.include_router(customers_router)
app.include_router(bikes_router)
app.include_router(service_router)
app.include_router(order_router)
app.include_router(bill_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
