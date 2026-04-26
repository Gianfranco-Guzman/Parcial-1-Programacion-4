from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response, status
from sqlmodel import Session

from backend.app.Core import (
    ConflictoDeNegocioError,
    RecursoNoEncontradoError,
    ValidacionDeServicioError,
    obtener_sesion,
)
from backend.app.Modules.Ingrediente.ingredienteSchema import (
    IngredienteActualizar,
    IngredienteCrear,
    IngredienteRespuesta,
)
from backend.app.Modules.Ingrediente.ingredienteService import servicio_ingrediente


router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])


@router.post("", response_model=IngredienteRespuesta, status_code=status.HTTP_201_CREATED)
def crear_ingrediente(
    datos_ingrediente: IngredienteCrear,
    sesion: Session = Depends(obtener_sesion),
) -> IngredienteRespuesta:
    try:
        return servicio_ingrediente.crear(sesion, datos_ingrediente)
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ConflictoDeNegocioError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except ValidacionDeServicioError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.get("", response_model=list[IngredienteRespuesta], status_code=status.HTTP_200_OK)
def listar_ingredientes(
    offset: Annotated[int, Query(ge=0, description="Cantidad de registros a omitir")] = 0,
    limite: Annotated[int, Query(ge=1, le=100, description="Cantidad máxima de resultados")] = 20,
    nombre: Annotated[str | None, Query(min_length=1, max_length=120, description="Filtro parcial por nombre")] = None,
    activo: Annotated[bool | None, Query(description="Filtra por estado activo/inactivo")] = None,
    calorias_minimas: Annotated[float | None, Query(ge=0, description="Filtra por calorías mínimas")] = None,
    sesion: Session = Depends(obtener_sesion),
) -> list[IngredienteRespuesta]:
    return servicio_ingrediente.listar(
        sesion,
        offset=offset,
        limite=limite,
        nombre=nombre,
        activo=activo,
        calorias_minimas=calorias_minimas,
    )


@router.get("/{id_ingrediente}", response_model=IngredienteRespuesta, status_code=status.HTTP_200_OK)
def obtener_ingrediente(
    id_ingrediente: Annotated[int, Path(gt=0, description="Identificador positivo del ingrediente")],
    sesion: Session = Depends(obtener_sesion),
) -> IngredienteRespuesta:
    try:
        return servicio_ingrediente.obtener_por_id(sesion, id_ingrediente)
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ConflictoDeNegocioError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except ValidacionDeServicioError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.put("/{id_ingrediente}", response_model=IngredienteRespuesta, status_code=status.HTTP_200_OK)
def actualizar_ingrediente(
    id_ingrediente: Annotated[int, Path(gt=0, description="Identificador positivo del ingrediente")],
    datos_ingrediente: IngredienteActualizar,
    sesion: Session = Depends(obtener_sesion),
) -> IngredienteRespuesta:
    try:
        return servicio_ingrediente.actualizar(sesion, id_ingrediente, datos_ingrediente)
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ConflictoDeNegocioError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except ValidacionDeServicioError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.delete("/{id_ingrediente}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ingrediente(
    id_ingrediente: Annotated[int, Path(gt=0, description="Identificador positivo del ingrediente")],
    sesion: Session = Depends(obtener_sesion),
) -> Response:
    try:
        servicio_ingrediente.eliminar(sesion, id_ingrediente)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except RecursoNoEncontradoError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ConflictoDeNegocioError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except ValidacionDeServicioError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
