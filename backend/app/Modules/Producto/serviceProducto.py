from datetime import datetime

from sqlalchemy.orm import selectinload
from sqlmodel import select

from backend.app.Core import (
    ConflictoDeNegocioError,
    RecursoNoEncontradoError,
    RepositorioBase,
    UnidadDeTrabajo,
    ValidacionDeServicioError,
)
from backend.app.Modules.Categoria.categoriaModel import Categoria
from backend.app.Modules.Ingrediente.ingredienteModel import Ingrediente
from backend.app.Modules.Producto.productoCategoriaModel import ProductoCategoria
from backend.app.Modules.Producto.productoIngredienteModel import ProductoIngrediente
from backend.app.Modules.Producto.productoModel import Producto
from backend.app.Modules.Producto.productoSchema import (
    IngredienteAsociadoCrear,
    ProductoActualizar,
    ProductoCrear,
)


class ServicioProducto:
    def __init__(self) -> None:
        self.repositorio = RepositorioBase(Producto)

    def listar(
        self,
        unidad_trabajo: UnidadDeTrabajo,
        offset: int = 0,
        limite: int = 100,
        nombre: str | None = None,
        disponible: bool | None = None,
        stock_minimo: int | None = None,
    ) -> list[Producto]:
        consulta = (
            select(Producto)
            .where(Producto.fecha_eliminacion == None)  # noqa: E711
            .options(selectinload(Producto.categorias))
            .options(selectinload(Producto.relaciones_ingrediente).selectinload(ProductoIngrediente.ingrediente))
        )

        if nombre:
            consulta = consulta.where(Producto.nombre.ilike(f"%{nombre}%"))

        if disponible is not None:
            consulta = consulta.where(Producto.disponible == disponible)

        if stock_minimo is not None:
            consulta = consulta.where(Producto.stock_cantidad >= stock_minimo)

        consulta = consulta.offset(offset).limit(limite)
        return list(unidad_trabajo.sesion.exec(consulta).all())

    def obtener_por_id(self, unidad_trabajo: UnidadDeTrabajo, id_producto: int) -> Producto:
        consulta = (
            select(Producto)
            .where(Producto.id == id_producto)
            .where(Producto.fecha_eliminacion == None)  # noqa: E711
            .options(selectinload(Producto.categorias))
            .options(selectinload(Producto.relaciones_ingrediente).selectinload(ProductoIngrediente.ingrediente))
        )
        producto = unidad_trabajo.sesion.exec(consulta).first()
        if producto is None:
            raise RecursoNoEncontradoError("El producto solicitado no existe")
        return producto

    def crear(self, unidad_trabajo: UnidadDeTrabajo, datos_producto: ProductoCrear) -> Producto:
        ids_categorias = self._normalizar_ids_categorias(datos_producto.ids_categorias)
        ingredientes_asociados = self._normalizar_ingredientes(datos_producto.ingredientes)

        categorias = self._obtener_categorias_por_ids(unidad_trabajo, ids_categorias)
        ingredientes = self._obtener_ingredientes_por_ids(
            unidad_trabajo,
            [ingrediente.id_ingrediente for ingrediente in ingredientes_asociados],
        )

        datos_base = datos_producto.model_dump(exclude={"ids_categorias", "ingredientes"})
        producto = Producto(**datos_base)

        self.repositorio.crear(unidad_trabajo.sesion, producto)
        producto.relaciones_categoria = self._construir_relaciones_categoria(categorias, producto.id)
        producto.relaciones_ingrediente = self._construir_relaciones_ingrediente(
            ingredientes,
            ingredientes_asociados,
            producto.id,
        )

        unidad_trabajo.sesion.add(producto)
        return self.obtener_por_id(unidad_trabajo, producto.id)

    def actualizar(self, unidad_trabajo: UnidadDeTrabajo, id_producto: int, datos_producto: ProductoActualizar) -> Producto:
        producto = self.obtener_por_id(unidad_trabajo, id_producto)
        datos_actualizacion = datos_producto.model_dump(exclude_unset=True)

        if "ids_categorias" in datos_actualizacion:
            ids_categorias = self._normalizar_ids_categorias(datos_actualizacion["ids_categorias"] or [])
            categorias = self._obtener_categorias_por_ids(unidad_trabajo, ids_categorias)
            producto.relaciones_categoria.clear()
            unidad_trabajo.sesion.flush()
            producto.relaciones_categoria = self._construir_relaciones_categoria(categorias, producto.id)

        if "ingredientes" in datos_actualizacion:
            ingredientes_asociados = self._normalizar_ingredientes_desde_actualizacion(
                datos_producto.ingredientes or []
            )
            ingredientes = self._obtener_ingredientes_por_ids(
                unidad_trabajo,
                [ingrediente.id_ingrediente for ingrediente in ingredientes_asociados],
            )
            producto.relaciones_ingrediente.clear()
            unidad_trabajo.sesion.flush()
            producto.relaciones_ingrediente = self._construir_relaciones_ingrediente(
                ingredientes,
                ingredientes_asociados,
                producto.id,
            )

        for campo, valor in datos_actualizacion.items():
            if campo in {"ids_categorias", "ingredientes"}:
                continue
            setattr(producto, campo, valor)

        producto.fecha_actualizacion = datetime.utcnow()
        unidad_trabajo.sesion.add(producto)
        return self.obtener_por_id(unidad_trabajo, producto.id)

    def eliminar(self, unidad_trabajo: UnidadDeTrabajo, id_producto: int) -> None:
        producto = self.obtener_por_id(unidad_trabajo, id_producto)
        self.repositorio.eliminar(unidad_trabajo.sesion, producto)

    def _normalizar_ids_categorias(self, ids_categorias: list[int]) -> list[int]:
        ids_normalizados = list(dict.fromkeys(ids_categorias))
        if len(ids_normalizados) != len(ids_categorias):
            raise ValidacionDeServicioError("No se pueden repetir categorías en un mismo producto")
        return ids_normalizados

    def _normalizar_ingredientes(
        self,
        ingredientes: list[IngredienteAsociadoCrear],
    ) -> list[IngredienteAsociadoCrear]:
        ids_ingredientes = [ingrediente.id_ingrediente for ingrediente in ingredientes]
        ids_unicos = list(dict.fromkeys(ids_ingredientes))

        if len(ids_unicos) != len(ids_ingredientes):
            raise ValidacionDeServicioError("No se pueden repetir ingredientes en un mismo producto")

        return ingredientes

    def _normalizar_ingredientes_desde_actualizacion(
        self,
        ingredientes: list[IngredienteAsociadoCrear],
    ) -> list[IngredienteAsociadoCrear]:
        return self._normalizar_ingredientes(ingredientes)

    def _obtener_categorias_por_ids(self, unidad_trabajo: UnidadDeTrabajo, ids_categorias: list[int]) -> list[Categoria]:
        if not ids_categorias:
            return []

        consulta = select(Categoria).where(Categoria.id.in_(ids_categorias)).where(Categoria.fecha_eliminacion == None)  # noqa: E711
        categorias = list(unidad_trabajo.sesion.exec(consulta).all())
        ids_encontrados = {categoria.id for categoria in categorias}
        ids_faltantes = [identificador for identificador in ids_categorias if identificador not in ids_encontrados]

        if ids_faltantes:
            raise RecursoNoEncontradoError(
                f"No existen las categorías con ids: {', '.join(str(valor) for valor in ids_faltantes)}"
            )

        categorias_por_id = {categoria.id: categoria for categoria in categorias}
        return [categorias_por_id[identificador] for identificador in ids_categorias]

    def _obtener_ingredientes_por_ids(self, unidad_trabajo: UnidadDeTrabajo, ids_ingredientes: list[int]) -> list[Ingrediente]:
        if not ids_ingredientes:
            return []

        consulta = select(Ingrediente).where(Ingrediente.id.in_(ids_ingredientes)).where(Ingrediente.fecha_eliminacion == None)  # noqa: E711
        ingredientes = list(unidad_trabajo.sesion.exec(consulta).all())
        ids_encontrados = {ingrediente.id for ingrediente in ingredientes}
        ids_faltantes = [identificador for identificador in ids_ingredientes if identificador not in ids_encontrados]

        if ids_faltantes:
            raise RecursoNoEncontradoError(
                f"No existen los ingredientes con ids: {', '.join(str(valor) for valor in ids_faltantes)}"
            )

        ingredientes_por_id = {ingrediente.id: ingrediente for ingrediente in ingredientes}
        return [ingredientes_por_id[identificador] for identificador in ids_ingredientes]

    def _construir_relaciones_categoria(
        self,
        categorias: list[Categoria],
        id_producto: int | None,
    ) -> list[ProductoCategoria]:
        if id_producto is None:
            raise ConflictoDeNegocioError("No se pudo persistir el producto antes de asociar categorías")

        enlaces: list[ProductoCategoria] = []
        for categoria in categorias:
            if categoria.id is None:
                raise RecursoNoEncontradoError("No se pudo asociar una categoría inexistente")

            enlaces.append(
                ProductoCategoria(
                    producto_id=id_producto,
                    categoria_id=categoria.id,
                )
            )

        return enlaces

    def _construir_relaciones_ingrediente(
        self,
        ingredientes: list[Ingrediente],
        ingredientes_asociados: list[IngredienteAsociadoCrear],
        id_producto: int | None,
    ) -> list[ProductoIngrediente]:
        if id_producto is None:
            raise ConflictoDeNegocioError("No se pudo persistir el producto antes de asociar ingredientes")

        ingredientes_por_id = {ingrediente.id: ingrediente for ingrediente in ingredientes}
        enlaces: list[ProductoIngrediente] = []

        for ingrediente_asociado in ingredientes_asociados:
            ingrediente = ingredientes_por_id.get(ingrediente_asociado.id_ingrediente)
            if ingrediente is None:
                raise RecursoNoEncontradoError("No se pudo asociar un ingrediente inexistente")

            enlaces.append(
                ProductoIngrediente(
                    producto_id=id_producto,
                    ingrediente_id=ingrediente_asociado.id_ingrediente,
                    cantidad=ingrediente_asociado.cantidad,
                )
            )

        return enlaces


servicio_producto = ServicioProducto()
