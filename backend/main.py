from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.Core.config import obtener_configuracion
from backend.app.Core.database import crear_tablas
from backend.app.Modules.Categoria.categoriaRouter import router as router_categoria
from backend.app.Modules.Ingrediente.ingredienteRouter import router as router_ingrediente
from backend.app.Modules.Producto.productoRouter import router as router_producto


configuracion = obtener_configuracion()



@asynccontextmanager
async def ciclo_de_vida(aplicacion: FastAPI):
    crear_tablas()
    yield


aplicacion = FastAPI(
    title=configuracion.titulo_api,
    description=configuracion.descripcion_api,
    version=configuracion.version_api,
    lifespan=ciclo_de_vida,
)

aplicacion.add_middleware(
    CORSMiddleware,
    allow_origins=list(configuracion.origenes_permitidos),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

aplicacion.include_router(router_producto, prefix=configuracion.prefijo_api)
aplicacion.include_router(router_categoria, prefix=configuracion.prefijo_api)
aplicacion.include_router(router_ingrediente, prefix=configuracion.prefijo_api)


@aplicacion.get("/")
def leer_raiz() -> dict[str, str]:
    return {"mensaje": "Backend del parcial operativo"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:aplicacion",
        host=configuracion.host,
        port=configuracion.puerto,
        reload=configuracion.modo_debug,
    )
