from sqlmodel import SQLModel, Field
from typing import Optional
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
