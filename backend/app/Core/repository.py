from datetime import datetime
from typing import Generic, TypeVar

from sqlmodel import Session, SQLModel, select


TipoModelo = TypeVar("TipoModelo", bound=SQLModel)


class RepositorioBase(Generic[TipoModelo]):
    def __init__(self, modelo: type[TipoModelo]) -> None:
        self.modelo = modelo

    def obtener_por_id(self, sesion: Session, identificador: int) -> TipoModelo | None:
        return sesion.get(self.modelo, identificador)

    def listar_todos(self, sesion: Session) -> list[TipoModelo]:
        consulta = select(self.modelo)
        return list(sesion.exec(consulta).all())

    def crear(self, sesion: Session, entidad: TipoModelo) -> TipoModelo:
        sesion.add(entidad)
        sesion.flush()
        sesion.refresh(entidad)
        return entidad

    def eliminar(self, sesion: Session, entidad: TipoModelo) -> None:
        if hasattr(entidad, "fecha_eliminacion"):
            entidad.fecha_eliminacion = datetime.utcnow()  # type: ignore[attr-defined]
            sesion.add(entidad)
            sesion.flush()
        else:
            sesion.delete(entidad)
