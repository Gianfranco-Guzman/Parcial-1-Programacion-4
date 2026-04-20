from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Ingrediente

router = APIRouter()

@router.post("/ingredientes")
def crear_ingrediente(nombre: str, descripcion: str = None, calorias_por_unidad: float = 0, db: Session = Depends(get_db)):
    db_ingrediente = Ingrediente(
        nombre=nombre, 
        descripcion=descripcion,
        calorias_por_unidad=calorias_por_unidad
    )
    db.add(db_ingrediente)
    db.commit()
    db.refresh(db_ingrediente)
    return db_ingrediente

@router.get("/ingredientes")
def listar_ingredientes(db: Session = Depends(get_db)):
    return db.query(Ingrediente).all()

@router.get("/ingredientes/{ingrediente_id}")
def obtener_ingrediente(ingrediente_id: int, db: Session = Depends(get_db)):
    db_ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if not db_ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return db_ingrediente

@router.delete("/ingredientes/{ingrediente_id}")
def eliminar_ingrediente(ingrediente_id: int, db: Session = Depends(get_db)):
    db_ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if not db_ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    
    db.delete(db_ingrediente)
    db.commit()
    return {"message": "Ingrediente eliminado"}
