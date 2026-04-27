from sqlmodel import select

from backend.app.Core import ConflictoDeNegocioError, RecursoNoEncontradoError, RepositorioBase, UnidadDeTrabajo
from backend.app.Modules.Categoria.categoriaModel import Categoria
from backend.app.Modules.Categoria.categoriaSchema import CategoriaActualizar, CategoriaCrear


class ServicioCategoria:
    def __init__(self) -> None:
        self.repositorio = RepositorioBase(Categoria)

    def listar(
        self,
        unidad_trabajo: UnidadDeTrabajo,
        offset: int = 0,
        limite: int = 100,
        nombre: str | None = None,
        activo: bool | None = None,
    ) -> list[Categoria]:
        consulta = select(Categoria)

        if nombre:
            consulta = consulta.where(Categoria.nombre.ilike(f"%{nombre}%"))

        if activo is not None:
            consulta = consulta.where(Categoria.activo == activo)

        consulta = consulta.offset(offset).limit(limite)
        return list(unidad_trabajo.sesion.exec(consulta).all())

    def obtener_por_id(self, unidad_trabajo: UnidadDeTrabajo, id_categoria: int) -> Categoria:
        categoria = self.repositorio.obtener_por_id(unidad_trabajo.sesion, id_categoria)
        if categoria is None:
            raise RecursoNoEncontradoError("La categoría solicitada no existe")
        return categoria

    def crear(self, unidad_trabajo: UnidadDeTrabajo, datos_categoria: CategoriaCrear) -> Categoria:
        self._validar_nombre_unico(unidad_trabajo, datos_categoria.nombre)
        categoria = Categoria(**datos_categoria.model_dump())
        self.repositorio.crear(unidad_trabajo.sesion, categoria)
        unidad_trabajo.sesion.refresh(categoria)
        return categoria

    def actualizar(self, unidad_trabajo: UnidadDeTrabajo, id_categoria: int, datos_categoria: CategoriaActualizar) -> Categoria:
        categoria = self.obtener_por_id(unidad_trabajo, id_categoria)
        datos_actualizacion = datos_categoria.model_dump(exclude_unset=True)

        nombre_nuevo = datos_actualizacion.get("nombre")
        if nombre_nuevo is not None and nombre_nuevo != categoria.nombre:
            self._validar_nombre_unico(unidad_trabajo, nombre_nuevo, id_categoria)

        for campo, valor in datos_actualizacion.items():
            setattr(categoria, campo, valor)

        unidad_trabajo.sesion.add(categoria)
        unidad_trabajo.sesion.refresh(categoria)
        return categoria

    def eliminar(self, unidad_trabajo: UnidadDeTrabajo, id_categoria: int) -> None:
        categoria = self.obtener_por_id(unidad_trabajo, id_categoria)
        self.repositorio.eliminar(unidad_trabajo.sesion, categoria)

    def _validar_nombre_unico(self, unidad_trabajo: UnidadDeTrabajo, nombre: str, id_categoria_actual: int | None = None) -> None:
        consulta = select(Categoria).where(Categoria.nombre == nombre)
        categoria_existente = unidad_trabajo.sesion.exec(consulta).first()

        if categoria_existente is None:
            return

        if id_categoria_actual is not None and categoria_existente.id == id_categoria_actual:
            return

        raise ConflictoDeNegocioError("Ya existe una categoría con ese nombre")


servicio_categoria = ServicioCategoria()
