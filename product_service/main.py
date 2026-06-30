from database import connection
from models import categorymodel, productmodel, productimgmodel
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router.product_router import router as product_router
from router.category_router import router as category_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

connection.Base.metadata.create_all(bind=connection.engine)

app = FastAPI()
app.mount(
    "/media",
    StaticFiles(directory="media"),
    name="media"
)
app.include_router(product_router, prefix='/api/v1/product')
app.include_router(category_router, prefix='/api/v1/category')
