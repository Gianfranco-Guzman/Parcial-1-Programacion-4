def formatear_precio(precio: float) -> str:
    return f"${precio:.2f}"

def validar_stock_positivo(stock: int) -> bool:
    return stock >= 0

def validar_precio_positivo(precio: float) -> bool:
    return precio > 0

def calcular_iva(precio: float, porcentaje: float = 21) -> float:
    return precio * (porcentaje / 100)

def obtener_precio_final(precio: float, porcentaje_iva: float = 21) -> float:
    iva = calcular_iva(precio, porcentaje_iva)
    return precio + iva
