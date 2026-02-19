from fastapi import FastAPI
from routes.product_routes import router


app= FastAPI(title="E-Commerce")

app.include_router(router)



