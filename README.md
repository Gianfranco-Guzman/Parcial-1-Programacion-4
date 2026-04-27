# Parcial 1 - Programación 4

## Descripción

Este proyecto implementa el **backend** del primer parcial de Programación 4 usando **FastAPI + SQLModel + PostgreSQL**.

La API permite gestionar:

- categorías
- ingredientes
- productos
- relaciones entre productos y categorías
- relaciones entre productos e ingredientes

Además, incluye:

- persistencia real en PostgreSQL
- relaciones complejas con tablas intermedias
- validaciones con `Annotated`, `Query` y `Path`
- separación por módulos (`routers`, `schemas`, `services`, `models`, `Core`)

> **Importante:** este repositorio actualmente contiene el backend. No incluye frontend.

---

## Tecnologías usadas

- Python
- FastAPI
- SQLModel
- SQLAlchemy
- PostgreSQL
- Uvicorn

---

## Estructura del proyecto

```text
backend/
├── app/
│   ├── Core/
│   └── Modules/
│       ├── Categoria/
│       ├── Ingrediente/
│       └── Producto/
└── main.py
```

---

## Requisitos

Antes de ejecutar el proyecto necesitás tener instalado:

- Python 3.11+ (recomendado)
- PostgreSQL

---

## Instalación

### 1. Crear y activar entorno virtual

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

---

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

---

### 3. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto.

Ejemplo:

```env
TITULO_API=API de Productos
DESCRIPCION_API=Backend del parcial para productos, categorías e ingredientes
VERSION_API=1.0.0
PREFIJO_API=/api
HOST_API=0.0.0.0
PUERTO_API=8000
MODO_DEBUG=true
ORIGENES_PERMITIDOS=*

ESQUEMA_BASE_DE_DATOS=postgresql+psycopg
USUARIO_BASE_DE_DATOS=postgres
CONTRASENA_BASE_DE_DATOS=123
HOST_BASE_DE_DATOS=localhost
PUERTO_BASE_DE_DATOS=5432
NOMBRE_BASE_DE_DATOS=parcial_programacion_4
```

Si preferís, podés tomar como base el archivo `.env.example`.

---

## Crear la base de datos

En PostgreSQL debe existir una base llamada:

```text
parcial_programacion_4
```

Si no existe, podés crearla manualmente desde pgAdmin, DBeaver o consola.

---

## Ejecución

### Ejecutar la API

```powershell
python -m uvicorn backend.main:aplicacion --host 127.0.0.1 --port 8000 --reload
```

---

## URLs importantes

- API: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`

---

## Funcionalidades disponibles

### Categorías
- crear
- listar
- obtener por id
- actualizar
- eliminar

### Ingredientes
- crear
- listar
- obtener por id
- actualizar
- eliminar

### Productos
- crear
- listar
- obtener por id
- actualizar
- eliminar

### Relaciones
- producto ↔ categoría
- producto ↔ ingrediente
- cantidad por ingrediente en producto

---

## Filtros y validaciones

La API incluye:

- paginación con `offset` y `limite`
- filtros por nombre
- filtros por estado `activo`
- filtros por `stock_minimo`
- filtros por `calorias_minimas`
- validaciones de `Path`
- validaciones de entrada con Pydantic/SQLModel

---

## Endpoints principales

### Categorías
- `POST /api/categorias`
- `GET /api/categorias`
- `GET /api/categorias/{id_categoria}`
- `PUT /api/categorias/{id_categoria}`
- `DELETE /api/categorias/{id_categoria}`

### Ingredientes
- `POST /api/ingredientes`
- `GET /api/ingredientes`
- `GET /api/ingredientes/{id_ingrediente}`
- `PUT /api/ingredientes/{id_ingrediente}`
- `DELETE /api/ingredientes/{id_ingrediente}`

### Productos
- `POST /api/productos`
- `GET /api/productos`
- `GET /api/productos/{id_producto}`
- `PUT /api/productos/{id_producto}`
- `DELETE /api/productos/{id_producto}`

---


## Video

Agregar acá el link al video cuando esté disponible:

```text
PENDIENTE
```

---

## Cambios y diagnóstico local

- Se corrigió un import circular entre `Core.database` y `Core.unit_of_work`: se movió la importación de `obtener_motor` para hacerse dentro de `UnidadDeTrabajo.__enter__` y se ajustaron imports en `backend/main.py` para evitar ejecutar `Core.__init__` durante el arranque.
- Se detectó un problema de autenticación al arrancar Uvicorn porque `URL_BASE_DE_DATOS` en el entorno estaba apuntando a una URL con la contraseña antigua (`postgres`). Solución: actualizar `URL_BASE_DE_DATOS` a la URL correcta o eliminarla para que la app use las variables individuales definidas en el `.env` (por ejemplo `CONTRASENA_BASE_DE_DATOS=admin123`).

Estas notas son cambios locales para facilitar el arranque en desarrollo y dejar trazabilidad de la depuración.
