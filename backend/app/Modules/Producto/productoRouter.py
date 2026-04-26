from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response, status
from sqlmodel import Session

from backend.app.Core import (
    ConflictoDeNegocioError,
    RecursoNoEncontradoError,
    ValidacionDeServicioError,
    obtener_sesion,
)
from backend.app.Modules.Producto.productoSchema import (
    ProductoActualizar,
    ProductoCrear,
    ProductoRespuestaRelacional,
)
from backend.app.Modules.Producto.serviceProducto import servicio_producto


router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("", response_model=ProductoRespuestaRelacional, status_code=status.HTTP_201_CREATED)
def crear_producto(
    datos_producto: ProductoCrear,
    sesion: Session = Depends(obtener_sesion),
) -> ProductoRespuestaRelacional:
    try:
        return servicio_producto.crear(sesion, datos_producto)
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ConflictoDeNegocioError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except ValidacionDeServicioError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.get("", response_model=list[ProductoRespuestaRelacional], status_code=status.HTTP_200_OK)
def listar_productos(
    offset: Annotated[int, Query(ge=0, description="Cantidad de registros a omitir")] = 0,
    limite: Annotated[int, Query(ge=1, le=100, description="Cantidad máxima de resultados")] = 20,
    nombre: Annotated[str | None, Query(min_length=1, max_length=120, description="Filtro parcial por nombre")] = None,
    activo: Annotated[bool | None, Query(description="Filtra por estado activo/inactivo")] = None,
    stock_minimo: Annotated[int | None, Query(ge=0, description="Filtra por stock mínimo")] = None,
    sesion: Session = Depends(obtener_sesion),
) -> list[ProductoRespuestaRelacional]:
    return servicio_producto.listar(
        sesion,
        offset=offset,
        limite=limite,
        nombre=nombre,
        activo=activo,
        stock_minimo=stock_minimo,
    )


@router.get("/{id_producto}", response_model=ProductoRespuestaRelacional, status_code=status.HTTP_200_OK)
def obtener_producto(
    id_producto: Annotated[int, Path(gt=0, description="Identificador positivo del producto")],
    sesion: Session = Depends(obtener_sesion),
) -> ProductoRespuestaRelacional:
    try:
        return servicio_producto.obtener_por_id(sesion, id_producto)
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ConflictoDeNegocioError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except ValidacionDeServicioError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.put("/{id_producto}", response_model=ProductoRespuestaRelacional, status_code=status.HTTP_200_OK)
def actualizar_producto(
    id_producto: Annotated[int, Path(gt=0, description="Identificador positivo del producto")],
    datos_producto: ProductoActualizar,
    sesion: Session = Depends(obtener_sesion),
) -> ProductoRespuestaRelacional:
    try:
        return servicio_producto.actualizar(sesion, id_producto, datos_producto)
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ConflictoDeNegocioError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except ValidacionDeServicioError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.delete("/{id_producto}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(
    id_producto: Annotated[int, Path(gt=0, description="Identificador positivo del producto")],
    sesion: Session = Depends(obtener_sesion),
) -> Response:
    try:
        servicio_producto.eliminar(sesion, id_producto)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ConflictoDeNegocioError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except ValidacionDeServicioError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
