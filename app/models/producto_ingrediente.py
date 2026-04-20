from sqlmodel import SQLModel, Field
from typing import Optional

class ProductoIngrediente(SQLModel, table=True):
    __tablename__ = "productos_ingredientes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    producto_id: int = Field(foreign_key="productos.id")
    ingrediente_id: int = Field(foreign_key="ingredientes.id")
    cantidad: float = Field(default=1.0)
