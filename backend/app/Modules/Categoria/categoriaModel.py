from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)
    descripcion: Optional[str] = None
    activo: bool = Field(default=True)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    
    productos: List["Producto"] = Relationship(
        back_populates="categorias",
        link_model="ProductoCategoria"
    )
