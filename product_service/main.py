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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # or restrict to specific origins, see note below
    allow_credentials=False,      # see note below
    allow_methods=["*"],          # GET, POST, PATCH, DELETE, OPTIONS, etc.
    allow_headers=["*"],          # lets your Authorization: Bearer header through
)
app.mount(
    "/media",
    StaticFiles(directory="media"),
    name="media"
)
app.include_router(product_router, prefix='/api/v1/product')
app.include_router(category_router, prefix='/api/v1/category')
