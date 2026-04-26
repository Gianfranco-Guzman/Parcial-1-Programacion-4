from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.app.Modules.Categoria.categoriaModel import Categoria
    from backend.app.Modules.Producto.productoModel import Producto


class ProductoCategoria(SQLModel, table=True):
    
    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categoria.id", primary_key=True)

    producto: Optional["Producto"] = Relationship(
        back_populates="relaciones_categoria",
        sa_relationship_kwargs={"overlaps": "categorias,productos,relaciones_producto"},         #sirve para las tablas intermedias
    )
    categoria: Optional["Categoria"] = Relationship(
        back_populates="relaciones_producto",
        sa_relationship_kwargs={"overlaps": "categorias,productos,relaciones_categoria"},   
    )
