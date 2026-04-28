from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import Field, Relationship, SQLModel

from backend.app.Modules.Producto.productoCategoriaModel import ProductoCategoria
from backend.app.Modules.Producto.productoIngredienteModel import ProductoIngrediente

if TYPE_CHECKING:
    from backend.app.Modules.Categoria.categoriaModel import Categoria
    from backend.app.Modules.Ingrediente.ingredienteModel import Ingrediente


class Producto(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, min_length=2, max_length=120)
    descripcion: Optional[str] = Field(default=None, max_length=500)
    precio_base: float = Field(ge=0)
    imagenes_url: Optional[List[str]] = Field(default=None, sa_column=Column(ARRAY(String), nullable=True))
    stock_cantidad: int = Field(default=0, ge=0)
    disponible: bool = Field(default=True)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_eliminacion: Optional[datetime] = Field(default=None)
    relaciones_categoria: List[ProductoCategoria] = Relationship(
        back_populates="producto",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},    #sirve para las tablas intermedias, cascade
    )
    relaciones_ingrediente: List[ProductoIngrediente] = Relationship(
        back_populates="producto",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    categorias: List["Categoria"] = Relationship(
        back_populates="productos",
        link_model=ProductoCategoria,
        sa_relationship_kwargs={
            "viewonly": True,
            "overlaps": "relaciones_categoria,producto,categoria,relaciones_producto",
        },
    )
    ingredientes: List["Ingrediente"] = Relationship(
        back_populates="productos",
        link_model=ProductoIngrediente,
        sa_relationship_kwargs={
            "viewonly": True,
            "overlaps": "relaciones_ingrediente,producto,ingrediente,relaciones_producto",
        },
    )
