from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from backend.app.Modules.Producto.productoIngredienteModel import ProductoIngrediente

if TYPE_CHECKING:
    from backend.app.Modules.Producto.productoModel import Producto


class Ingrediente(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True, min_length=2, max_length=120)
    descripcion: Optional[str] = Field(default=None, max_length=300)
    calorias_por_unidad: float = Field(default=0, ge=0)
    activo: bool = Field(default=True)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)

    relaciones_producto: List[ProductoIngrediente] = Relationship(
        back_populates="ingrediente",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    productos: List["Producto"] = Relationship(
        back_populates="ingredientes",
        link_model=ProductoIngrediente,
        sa_relationship_kwargs={
            "viewonly": True,
            "overlaps": "relaciones_producto,ingrediente,producto,relaciones_ingrediente",
        },
    )
