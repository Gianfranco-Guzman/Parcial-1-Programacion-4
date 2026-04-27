from collections.abc import Generator
from functools import lru_cache

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, SQLModel, create_engine

from backend.app.Core.config import obtener_configuracion
from backend.app.Core.unit_of_work import UnidadDeTrabajo


configuracion = obtener_configuracion()

argumentos_conexion: dict[str, object] = {}
if configuracion.url_base_de_datos.startswith("sqlite"):
    argumentos_conexion["check_same_thread"] = False


@lru_cache
def obtener_motor():
    return create_engine(
        configuracion.url_base_de_datos,
        echo=configuracion.modo_debug,
        pool_pre_ping=True,
        connect_args=argumentos_conexion,
    )


def crear_tablas() -> None:
    from backend.app.Modules.Categoria.categoriaModel import Categoria
    from backend.app.Modules.Ingrediente.ingredienteModel import Ingrediente
    from backend.app.Modules.Producto.productoCategoriaModel import ProductoCategoria
    from backend.app.Modules.Producto.productoIngredienteModel import ProductoIngrediente
    from backend.app.Modules.Producto.productoModel import Producto

    _ = (Categoria, Ingrediente, ProductoCategoria, ProductoIngrediente, Producto)
    SQLModel.metadata.create_all(obtener_motor())


def obtener_sesion() -> Generator[Session, None, None]:
    with Session(obtener_motor()) as sesion:
        yield sesion


def obtener_unidad_trabajo() -> Generator[UnidadDeTrabajo, None, None]:
    with UnidadDeTrabajo() as unidad:
        yield unidad


def probar_conexion_base_de_datos() -> tuple[bool, str]:
    try:
        with obtener_motor().connect() as conexion:
            conexion.execute(text("SELECT 1"))
        return True, "Conexión a PostgreSQL verificada correctamente"
    except SQLAlchemyError as error:
        mensaje_error = str(error).encode("cp1252", errors="replace").decode("cp1252")
        return False, f"No se pudo verificar la conexión a la base de datos: {mensaje_error}"
