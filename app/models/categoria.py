from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Categoria(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)
    descripcion: Optional[str] = None
    activo: bool = Field(default=True)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
