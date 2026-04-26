from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class IngredienteBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    descripcion: str | None = Field(default=None, max_length=300)
    calorias_por_unidad: float = Field(default=0, ge=0)
    activo: bool = True


class IngredienteCrear(IngredienteBase):
    pass


class IngredienteActualizar(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=120)
    descripcion: str | None = Field(default=None, max_length=300)
    calorias_por_unidad: float | None = Field(default=None, ge=0)
    activo: bool | None = None


class IngredienteSimple(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str


class IngredienteRespuesta(IngredienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_creacion: datetime


class IngredienteProductoDetalle(IngredienteRespuesta):
    cantidad: float = Field(gt=0)
