class ErrorDeServicio(Exception):
    """Error base para la capa de servicios."""


class RecursoNoEncontradoError(ErrorDeServicio):
    """Se dispara cuando no existe un recurso buscado."""


class ConflictoDeNegocioError(ErrorDeServicio):
    """Se dispara cuando una regla de negocio impide la operación."""


class ValidacionDeServicioError(ErrorDeServicio):
    """Se dispara cuando los datos no cumplen validaciones del servicio."""
