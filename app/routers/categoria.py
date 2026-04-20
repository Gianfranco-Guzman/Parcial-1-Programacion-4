from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Categoria

router = APIRouter()

@router.post("/categorias")
def crear_categoria(nombre: str, descripcion: str = None, db: Session = Depends(get_db)):
    db_categoria = Categoria(nombre=nombre, descripcion=descripcion)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@router.get("/categorias")
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

@router.get("/categorias/{categoria_id}")
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria

@router.delete("/categorias/{categoria_id}")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    db.delete(db_categoria)
    db.commit()
    return {"message": "Categoría eliminada"}
