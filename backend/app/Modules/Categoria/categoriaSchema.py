from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class CategoriaBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    descripcion: str | None = Field(default=None, max_length=300)
    imagen_url: str | None = Field(default=None, max_length=500)
    activo: bool = True
    categoria_padre_id: int | None = None


class CategoriaCrear(CategoriaBase):
    pass


class CategoriaActualizar(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=120)
    descripcion: str | None = Field(default=None, max_length=300)
    imagen_url: str | None = Field(default=None, max_length=500)
    activo: bool | None = None
    categoria_padre_id: int | None = None


class CategoriaSimple(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str


class CategoriaRespuesta(CategoriaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    subcategorias: List[CategoriaSimple] = []
