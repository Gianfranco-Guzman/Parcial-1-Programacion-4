from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.app.Modules.Ingrediente.ingredienteModel import Ingrediente
    from backend.app.Modules.Producto.productoModel import Producto


class ProductoIngrediente(SQLModel, table=True):

    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    ingrediente_id: int = Field(foreign_key="ingrediente.id", primary_key=True)
    cantidad: float = Field(default=1.0, gt=0)

    # es removible
    producto: Optional["Producto"] = Relationship(
        back_populates="relaciones_ingrediente",
        sa_relationship_kwargs={"overlaps": "ingredientes,productos,relaciones_producto"},          #sirve para las tablas intermedias
    )
    ingrediente: Optional["Ingrediente"] = Relationship(
        back_populates="relaciones_producto",
        sa_relationship_kwargs={"overlaps": "ingredientes,productos,relaciones_ingrediente"},
    )
