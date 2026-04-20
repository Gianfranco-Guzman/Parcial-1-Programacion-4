from sqlmodel import SQLModel, Field
from typing import Optional


class ProductoCategoria(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    producto_id: int = Field(foreign_key="productos.id")
    categoria_id: int = Field(foreign_key="categorias.id")
