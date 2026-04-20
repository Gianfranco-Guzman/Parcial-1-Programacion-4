from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse

router = APIRouter()

@router.post("/productos", response_model=ProductoResponse)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.get("/productos", response_model=list[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()

@router.get("/productos/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@router.put("/productos/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    update_data = producto.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_producto, key, value)
    
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(db_producto)
    db.commit()
    return {"message": "Producto eliminado"}
