from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response, status
from sqlmodel import Session

from backend.app.Core import (
    ConflictoDeNegocioError,
    RecursoNoEncontradoError,
    ValidacionDeServicioError,
    obtener_sesion,
)
from backend.app.Modules.Categoria.categoriaSchema import (
    CategoriaActualizar,
    CategoriaCrear,
    CategoriaRespuesta,
)
from backend.app.Modules.Categoria.categoriaService import servicio_categoria


router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.post("", response_model=CategoriaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_categoria(
    datos_categoria: CategoriaCrear,
    sesion: Session = Depends(obtener_sesion),
) -> CategoriaRespuesta:
    try:
        return servicio_categoria.crear(sesion, datos_categoria)
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ConflictoDeNegocioError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except ValidacionDeServicioError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.get("", response_model=list[CategoriaRespuesta], status_code=status.HTTP_200_OK)
def listar_categorias(
    offset: Annotated[int, Query(ge=0, description="Cantidad de registros a omitir")] = 0,
    limite: Annotated[int, Query(ge=1, le=100, description="Cantidad máxima de resultados")] = 20,
    nombre: Annotated[str | None, Query(min_length=1, max_length=120, description="Filtro parcial por nombre")] = None,
    activo: Annotated[bool | None, Query(description="Filtra por estado activo/inactivo")] = None,
    sesion: Session = Depends(obtener_sesion),
) -> list[CategoriaRespuesta]:
    return servicio_categoria.listar(sesion, offset=offset, limite=limite, nombre=nombre, activo=activo)


@router.get("/{id_categoria}", response_model=CategoriaRespuesta, status_code=status.HTTP_200_OK)
def obtener_categoria(
    id_categoria: Annotated[int, Path(gt=0, description="Identificador positivo de la categoría")],
    sesion: Session = Depends(obtener_sesion),
) -> CategoriaRespuesta:
    try:
        return servicio_categoria.obtener_por_id(sesion, id_categoria)
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ConflictoDeNegocioError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except ValidacionDeServicioError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.put("/{id_categoria}", response_model=CategoriaRespuesta, status_code=status.HTTP_200_OK)
def actualizar_categoria(
    id_categoria: Annotated[int, Path(gt=0, description="Identificador positivo de la categoría")],
    datos_categoria: CategoriaActualizar,
    sesion: Session = Depends(obtener_sesion),
) -> CategoriaRespuesta:
    try:
        return servicio_categoria.actualizar(sesion, id_categoria, datos_categoria)
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ConflictoDeNegocioError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except ValidacionDeServicioError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.delete("/{id_categoria}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(
    id_categoria: Annotated[int, Path(gt=0, description="Identificador positivo de la categoría")],
    sesion: Session = Depends(obtener_sesion),
) -> Response:
    try:
        servicio_categoria.eliminar(sesion, id_categoria)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ConflictoDeNegocioError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except ValidacionDeServicioError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
