from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from backend.app.Modules.Producto.productoCategoriaModel import ProductoCategoria

if TYPE_CHECKING:
    from backend.app.Modules.Producto.productoModel import Producto


class Categoria(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True, min_length=2, max_length=120)
    descripcion: Optional[str] = Field(default=None, max_length=300)
    imagen_url: Optional[str] = Field(default=None, max_length=500)
    activo: bool = Field(default=True)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_eliminacion: Optional[datetime] = Field(default=None)
    categoria_padre_id: Optional[int] = Field(default=None, foreign_key="categoria.id")

    subcategorias: List["Categoria"] = Relationship(
        back_populates="categoria_padre",
        sa_relationship_kwargs={
            "foreign_keys": "[Categoria.categoria_padre_id]",
            "lazy": "select",
        },
    )
    categoria_padre: Optional["Categoria"] = Relationship(
        back_populates="subcategorias",
        sa_relationship_kwargs={
            "foreign_keys": "[Categoria.categoria_padre_id]",
            "remote_side": "[Categoria.id]",
            "lazy": "select",
        },
    )

    relaciones_producto: List[ProductoCategoria] = Relationship(
        back_populates="categoria",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    productos: List["Producto"] = Relationship(
        back_populates="categorias",
        link_model=ProductoCategoria,
        sa_relationship_kwargs={
            "viewonly": True,
            "overlaps": "relaciones_producto,categoria,producto,relaciones_categoria",
        },
    )
