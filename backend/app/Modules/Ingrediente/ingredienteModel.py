from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Ingrediente(SQLModel, table=True):
    __tablename__ = "ingredientes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)
    descripcion: Optional[str] = None
    calorias_por_unidad: float = Field(default=0)
    activo: bool = Field(default=True)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    
    productos: List["Producto"] = Relationship(
        back_populates="ingredientes",
        link_model="ProductoIngrediente"
    )
