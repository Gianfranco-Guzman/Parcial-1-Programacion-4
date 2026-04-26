from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path


RUTA_RAIZ_PROYECTO = Path(__file__).resolve().parents[3]


def _cargar_archivo_entorno() -> None:
    rutas_entorno = [
        RUTA_RAIZ_PROYECTO / ".env",
        RUTA_RAIZ_PROYECTO / ".env.local",
    ]

    for ruta_entorno in rutas_entorno:
        if not ruta_entorno.exists():
            continue

        for linea in ruta_entorno.read_text(encoding="utf-8").splitlines():
            linea_limpia = linea.strip()
            if not linea_limpia or linea_limpia.startswith("#") or "=" not in linea_limpia:
                continue

            clave, valor = linea_limpia.split("=", 1)
            clave = clave.strip()
            valor = valor.strip().strip('"').strip("'")

            if clave:
                os.environ.setdefault(clave, valor)


_cargar_archivo_entorno()


@dataclass(frozen=True)
class Configuracion:
    titulo_api: str = "API de Productos"
    descripcion_api: str = "Backend del parcial para productos, categorías e ingredientes"
    version_api: str = "1.0.0"
    prefijo_api: str = "/api"
    host: str = "0.0.0.0"
    puerto: int = 8000
    modo_debug: bool = False
    esquema_base_de_datos: str = "postgresql+psycopg"
    usuario_base_de_datos: str = "postgres"
    contrasena_base_de_datos: str = "postgres"
    host_base_de_datos: str = "localhost"
    puerto_base_de_datos: int = 5432
    nombre_base_de_datos: str = "parcial_programacion_4"
    url_base_de_datos: str = "postgresql+psycopg://postgres:postgres@localhost:5432/parcial_programacion_4"
    origenes_permitidos: tuple[str, ...] = ("*",)


def _construir_url_base_de_datos() -> str:
    url_explicitada = os.getenv("URL_BASE_DE_DATOS")
    if url_explicitada:
        return url_explicitada

    esquema_base_de_datos = os.getenv("ESQUEMA_BASE_DE_DATOS", "postgresql+psycopg")
    usuario_base_de_datos = os.getenv("USUARIO_BASE_DE_DATOS", "postgres")
    contrasena_base_de_datos = os.getenv("CONTRASENA_BASE_DE_DATOS", "postgres")
    host_base_de_datos = os.getenv("HOST_BASE_DE_DATOS", "localhost")
    puerto_base_de_datos = os.getenv("PUERTO_BASE_DE_DATOS", "5432")
    nombre_base_de_datos = os.getenv("NOMBRE_BASE_DE_DATOS", "parcial_programacion_4")

    return (
        f"{esquema_base_de_datos}://{usuario_base_de_datos}:{contrasena_base_de_datos}"
        f"@{host_base_de_datos}:{puerto_base_de_datos}/{nombre_base_de_datos}"
    )


def _texto_a_booleano(valor: str | None, valor_por_defecto: bool = False) -> bool:
    if valor is None:
        return valor_por_defecto

    return valor.strip().lower() in {"1", "true", "t", "si", "sí", "yes", "y", "on"}


@lru_cache
def obtener_configuracion() -> Configuracion:
    return Configuracion(
        titulo_api=os.getenv("TITULO_API", "API de Productos"),
        descripcion_api=os.getenv(
            "DESCRIPCION_API",
            "Backend del parcial para productos, categorías e ingredientes",
        ),
        version_api=os.getenv("VERSION_API", "1.0.0"),
        prefijo_api=os.getenv("PREFIJO_API", "/api"),
        host=os.getenv("HOST_API", "0.0.0.0"),
        puerto=int(os.getenv("PUERTO_API", "8000")),
        modo_debug=_texto_a_booleano(os.getenv("MODO_DEBUG"), False),
        esquema_base_de_datos=os.getenv("ESQUEMA_BASE_DE_DATOS", "postgresql+psycopg"),
        usuario_base_de_datos=os.getenv("USUARIO_BASE_DE_DATOS", "postgres"),
        contrasena_base_de_datos=os.getenv("CONTRASENA_BASE_DE_DATOS", "postgres"),
        host_base_de_datos=os.getenv("HOST_BASE_DE_DATOS", "localhost"),
        puerto_base_de_datos=int(os.getenv("PUERTO_BASE_DE_DATOS", "5432")),
        nombre_base_de_datos=os.getenv("NOMBRE_BASE_DE_DATOS", "parcial_programacion_4"),
        url_base_de_datos=_construir_url_base_de_datos(),
        origenes_permitidos=tuple(
            origen.strip()
            for origen in os.getenv("ORIGENES_PERMITIDOS", "*").split(",")
            if origen.strip()
        ) or ("*",),
    )
