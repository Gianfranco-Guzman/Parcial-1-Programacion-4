from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Ingrediente(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)
    descripcion: Optional[str] = None
    calorias_por_unidad: float = Field(default=0)
    activo: bool = Field(default=True)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
