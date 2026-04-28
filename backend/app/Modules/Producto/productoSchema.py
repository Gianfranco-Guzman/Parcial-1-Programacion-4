from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.app.Modules.Categoria.categoriaSchema import CategoriaRespuesta, CategoriaSimple
from backend.app.Modules.Ingrediente.ingredienteSchema import (
    IngredienteProductoDetalle,
    IngredienteRespuesta,
    IngredienteSimple,
)


class ProductoBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    descripcion: str | None = Field(default=None, max_length=500)
    precio_base: float = Field(ge=0)
    imagenes_url: list[str] | None = None
    stock_cantidad: int = Field(default=0, ge=0)
    disponible: bool = True


class ProductoCrear(ProductoBase):
    ids_categorias: list[int] = Field(default_factory=list)
    ingredientes: list["IngredienteAsociadoCrear"] = Field(default_factory=list)


class ProductoActualizar(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=120)
    descripcion: str | None = Field(default=None, max_length=500)
    precio_base: float | None = Field(default=None, ge=0)
    imagenes_url: list[str] | None = None
    stock_cantidad: int | None = Field(default=None, ge=0)
    disponible: bool | None = None
    ids_categorias: list[int] | None = None
    ingredientes: list["IngredienteAsociadoCrear"] | None = None


class ProductoSimple(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str


class IngredienteAsociadoCrear(BaseModel):
    id_ingrediente: int = Field(gt=0)
    cantidad: float = Field(gt=0)


class ProductoRespuesta(ProductoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime


class ProductoRespuestaDetalle(ProductoRespuesta):
    categorias: list[CategoriaSimple] = Field(default_factory=list)
    ingredientes: list[IngredienteRespuesta] = Field(default_factory=list)


class RelacionProductoIngredienteRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cantidad: float
    es_removible: bool
    ingrediente: IngredienteSimple


class ProductoRespuestaRelacional(ProductoRespuesta):
    categorias: list[CategoriaRespuesta] = Field(default_factory=list)
    relaciones_ingrediente: list[RelacionProductoIngredienteRespuesta] = Field(default_factory=list)


class ProductoRespuestaParaListado(ProductoRespuesta):
    categorias: list[CategoriaSimple] = Field(default_factory=list)
    ingredientes: list[IngredienteProductoDetalle] = Field(default_factory=list)


ProductoCrear.model_rebuild()
ProductoActualizar.model_rebuild()
