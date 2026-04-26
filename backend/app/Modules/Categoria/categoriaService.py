from sqlmodel import Session, select

from backend.app.Core import ConflictoDeNegocioError, RecursoNoEncontradoError, RepositorioBase
from backend.app.Modules.Categoria.categoriaModel import Categoria
from backend.app.Modules.Categoria.categoriaSchema import CategoriaActualizar, CategoriaCrear


class ServicioCategoria:
    def __init__(self) -> None:
        self.repositorio = RepositorioBase(Categoria)

    def listar(
        self,
        sesion: Session,
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
        return list(sesion.exec(consulta).all())

    def obtener_por_id(self, sesion: Session, id_categoria: int) -> Categoria:
        categoria = self.repositorio.obtener_por_id(sesion, id_categoria)
        if categoria is None:
            raise RecursoNoEncontradoError("La categoría solicitada no existe")
        return categoria

    def crear(self, sesion: Session, datos_categoria: CategoriaCrear) -> Categoria:
        self._validar_nombre_unico(sesion, datos_categoria.nombre)
        categoria = Categoria(**datos_categoria.model_dump())
        self.repositorio.crear(sesion, categoria)
        sesion.commit()
        sesion.refresh(categoria)
        return categoria

    def actualizar(self, sesion: Session, id_categoria: int, datos_categoria: CategoriaActualizar) -> Categoria:
        categoria = self.obtener_por_id(sesion, id_categoria)
        datos_actualizacion = datos_categoria.model_dump(exclude_unset=True)

        nombre_nuevo = datos_actualizacion.get("nombre")
        if nombre_nuevo is not None and nombre_nuevo != categoria.nombre:
            self._validar_nombre_unico(sesion, nombre_nuevo, id_categoria)

        for campo, valor in datos_actualizacion.items():
            setattr(categoria, campo, valor)

        sesion.add(categoria)
        sesion.commit()
        sesion.refresh(categoria)
        return categoria

    def eliminar(self, sesion: Session, id_categoria: int) -> None:
        categoria = self.obtener_por_id(sesion, id_categoria)
        self.repositorio.eliminar(sesion, categoria)
        sesion.commit()

    def _validar_nombre_unico(self, sesion: Session, nombre: str, id_categoria_actual: int | None = None) -> None:
        consulta = select(Categoria).where(Categoria.nombre == nombre)
        categoria_existente = sesion.exec(consulta).first()

        if categoria_existente is None:
            return

        if id_categoria_actual is not None and categoria_existente.id == id_categoria_actual:
            return

        raise ConflictoDeNegocioError("Ya existe una categoría con ese nombre")


servicio_categoria = ServicioCategoria()
