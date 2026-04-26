from __future__ import annotations

from sqlmodel import Session

from backend.app.Core.database import obtener_motor


class UnidadDeTrabajo:
    def __init__(self) -> None:
        self.sesion: Session | None = None

    def __enter__(self) -> "UnidadDeTrabajo":
        self.sesion = Session(obtener_motor())
        return self

    def __exit__(self, tipo_excepcion, valor_excepcion, traceback_excepcion) -> None:
        if self.sesion is None:
            return

        if tipo_excepcion is not None:
            self.sesion.rollback()
        else:
            self.sesion.commit()

        self.sesion.close()
        self.sesion = None

    def confirmar(self) -> None:
        if self.sesion is None:
            raise RuntimeError("La sesión de la unidad de trabajo no fue inicializada")
        self.sesion.commit()

    def deshacer(self) -> None:
        if self.sesion is None:
            raise RuntimeError("La sesión de la unidad de trabajo no fue inicializada")
        self.sesion.rollback()
