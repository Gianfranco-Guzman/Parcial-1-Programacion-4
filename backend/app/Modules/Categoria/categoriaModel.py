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
    activo: bool = Field(default=True)
    # imagen url
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    # parent ir. Relacion reflexiva para categorias hijas
    # fecha update
    # fecha delete

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
