from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

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
    precio: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)
    activo: bool = Field(default=True)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: datetime = Field(default_factory=datetime.utcnow)

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
