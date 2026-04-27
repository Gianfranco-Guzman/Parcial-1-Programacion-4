from sqlmodel import select

from backend.app.Core import ConflictoDeNegocioError, RecursoNoEncontradoError, RepositorioBase, UnidadDeTrabajo
from backend.app.Modules.Ingrediente.ingredienteModel import Ingrediente
from backend.app.Modules.Ingrediente.ingredienteSchema import IngredienteActualizar, IngredienteCrear


class ServicioIngrediente:
    def __init__(self) -> None:
        self.repositorio = RepositorioBase(Ingrediente)

    def listar(
        self,
        unidad_trabajo: UnidadDeTrabajo,
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
        return list(unidad_trabajo.sesion.exec(consulta).all())

    def obtener_por_id(self, unidad_trabajo: UnidadDeTrabajo, id_ingrediente: int) -> Ingrediente:
        ingrediente = self.repositorio.obtener_por_id(unidad_trabajo.sesion, id_ingrediente)
        if ingrediente is None:
            raise RecursoNoEncontradoError("El ingrediente solicitado no existe")
        return ingrediente

    def crear(self, unidad_trabajo: UnidadDeTrabajo, datos_ingrediente: IngredienteCrear) -> Ingrediente:
        self._validar_nombre_unico(unidad_trabajo, datos_ingrediente.nombre)
        ingrediente = Ingrediente(**datos_ingrediente.model_dump())
        self.repositorio.crear(unidad_trabajo.sesion, ingrediente)
        unidad_trabajo.sesion.refresh(ingrediente)
        return ingrediente

    def actualizar(self, unidad_trabajo: UnidadDeTrabajo, id_ingrediente: int, datos_ingrediente: IngredienteActualizar) -> Ingrediente:
        ingrediente = self.obtener_por_id(unidad_trabajo, id_ingrediente)
        datos_actualizacion = datos_ingrediente.model_dump(exclude_unset=True)

        nombre_nuevo = datos_actualizacion.get("nombre")
        if nombre_nuevo is not None and nombre_nuevo != ingrediente.nombre:
            self._validar_nombre_unico(unidad_trabajo, nombre_nuevo, id_ingrediente)

        for campo, valor in datos_actualizacion.items():
            setattr(ingrediente, campo, valor)

        unidad_trabajo.sesion.add(ingrediente)
        unidad_trabajo.sesion.refresh(ingrediente)
        return ingrediente

    def eliminar(self, unidad_trabajo: UnidadDeTrabajo, id_ingrediente: int) -> None:
        ingrediente = self.obtener_por_id(unidad_trabajo, id_ingrediente)
        self.repositorio.eliminar(unidad_trabajo.sesion, ingrediente)

    def _validar_nombre_unico(self, unidad_trabajo: UnidadDeTrabajo, nombre: str, id_ingrediente_actual: int | None = None) -> None:
        consulta = select(Ingrediente).where(Ingrediente.nombre == nombre)
        ingrediente_existente = unidad_trabajo.sesion.exec(consulta).first()

        if ingrediente_existente is None:
            return

        if id_ingrediente_actual is not None and ingrediente_existente.id == id_ingrediente_actual:
            return

        raise ConflictoDeNegocioError("Ya existe un ingrediente con ese nombre")


servicio_ingrediente = ServicioIngrediente()
