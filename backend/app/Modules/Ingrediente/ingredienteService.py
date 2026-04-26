from sqlmodel import Session, select

from backend.app.Core import ConflictoDeNegocioError, RecursoNoEncontradoError, RepositorioBase
from backend.app.Modules.Ingrediente.ingredienteModel import Ingrediente
from backend.app.Modules.Ingrediente.ingredienteSchema import IngredienteActualizar, IngredienteCrear


class ServicioIngrediente:
    def __init__(self) -> None:
        self.repositorio = RepositorioBase(Ingrediente)

    def listar(
        self,
        sesion: Session,
        offset: int = 0,
        limite: int = 100,
        nombre: str | None = None,
        activo: bool | None = None,
        calorias_minimas: float | None = None,
    ) -> list[Ingrediente]:
        consulta = select(Ingrediente)

        if nombre:
            consulta = consulta.where(Ingrediente.nombre.ilike(f"%{nombre}%"))

        if activo is not None:
            consulta = consulta.where(Ingrediente.activo == activo)

        if calorias_minimas is not None:
            consulta = consulta.where(Ingrediente.calorias_por_unidad >= calorias_minimas)

        consulta = consulta.offset(offset).limit(limite)
        return list(sesion.exec(consulta).all())

    def obtener_por_id(self, sesion: Session, id_ingrediente: int) -> Ingrediente:
        ingrediente = self.repositorio.obtener_por_id(sesion, id_ingrediente)
        if ingrediente is None:
            raise RecursoNoEncontradoError("El ingrediente solicitado no existe")
        return ingrediente

    def crear(self, sesion: Session, datos_ingrediente: IngredienteCrear) -> Ingrediente:
        self._validar_nombre_unico(sesion, datos_ingrediente.nombre)
        ingrediente = Ingrediente(**datos_ingrediente.model_dump())
        self.repositorio.crear(sesion, ingrediente)
        sesion.commit()
        sesion.refresh(ingrediente)
        return ingrediente

    def actualizar(self, sesion: Session, id_ingrediente: int, datos_ingrediente: IngredienteActualizar) -> Ingrediente:
        ingrediente = self.obtener_por_id(sesion, id_ingrediente)
        datos_actualizacion = datos_ingrediente.model_dump(exclude_unset=True)

        nombre_nuevo = datos_actualizacion.get("nombre")
        if nombre_nuevo is not None and nombre_nuevo != ingrediente.nombre:
            self._validar_nombre_unico(sesion, nombre_nuevo, id_ingrediente)

        for campo, valor in datos_actualizacion.items():
            setattr(ingrediente, campo, valor)

        sesion.add(ingrediente)
        sesion.commit()
        sesion.refresh(ingrediente)
        return ingrediente

    def eliminar(self, sesion: Session, id_ingrediente: int) -> None:
        ingrediente = self.obtener_por_id(sesion, id_ingrediente)
        self.repositorio.eliminar(sesion, ingrediente)
        sesion.commit()

    def _validar_nombre_unico(self, sesion: Session, nombre: str, id_ingrediente_actual: int | None = None) -> None:
        consulta = select(Ingrediente).where(Ingrediente.nombre == nombre)
        ingrediente_existente = sesion.exec(consulta).first()

        if ingrediente_existente is None:
            return

        if id_ingrediente_actual is not None and ingrediente_existente.id == id_ingrediente_actual:
            return

        raise ConflictoDeNegocioError("Ya existe un ingrediente con ese nombre")


servicio_ingrediente = ServicioIngrediente()
