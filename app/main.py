from fastapi import FastAPI
from app.database import engine, Base
from app.routers import producto_router, categoria_router, ingrediente_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Productos",
    description="API para gestionar productos, categorías e ingredientes",
    version="1.0.0"
)

app.include_router(producto_router, prefix="/api", tags=["productos"])
app.include_router(categoria_router, prefix="/api", tags=["categorias"])
app.include_router(ingrediente_router, prefix="/api", tags=["ingredientes"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Productos"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
