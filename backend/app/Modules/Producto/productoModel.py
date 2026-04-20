from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Producto(SQLModel, table=True):
    __tablename__ = "productos"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    descripcion: Optional[str] = None
    precio: float
    stock: int = Field(default=0)
    activo: bool = Field(default=True)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: datetime = Field(default_factory=datetime.utcnow)
    
    categorias: List["Categoria"] = Relationship(
        back_populates="productos",
        link_model="ProductoCategoria"
    )
    ingredientes: List["Ingrediente"] = Relationship(
        back_populates="productos",
        link_model="ProductoIngrediente"
    )
