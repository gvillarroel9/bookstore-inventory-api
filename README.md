
# API de Inventario para Librerías

Este proyecto es una API basada en Django para la gestión de inventario de una librería. Permite operaciones CRUD sobre libros y se integra con una base de datos PostgreSQL.

## Requisitos previos

- Docker
- Docker Compose

## Instalación

1. Clona el repositorio:

   ```
   git clone https://github.com/gvillarroel9/bookstore-inventory-api
   cd bookstore-inventory-api
   ```


2. Levanta primero el contenedor de la base de datos:

   ```
   docker-compose up -d db
   ```

3. Ejecuta las migraciones para preparar la base de datos:

   ```
   docker-compose run web python manage.py migrate
   ```

4. Levanta la aplicación:

   ```
   docker-compose up --build web
   ```

## Uso


Una vez que la aplicación está corriendo, puedes acceder a la API en `http://localhost:8000/api/`.

> **Nota:** Este repositorio incluye el archivo `Bookstore-Inventory-API.postman_collection.json` para importar en Postman y facilitar las pruebas de los endpoints si lo deseas.

### Endpoints principales

- **GET /api/books/**: Listar todos los libros.
- **POST /api/books/**: Crear un nuevo libro.
- **GET /api/books/{id}/**: Obtener un libro por ID.
- **PUT /api/books/{id}/**: Actualizar un libro por ID.
- **DELETE /api/books/{id}/**: Eliminar un libro por ID.

### Endpoints adicionales

- **GET /api/books/search?category={categoria}**: Buscar libros por categoría (búsqueda flexible).
- **GET /api/books/low-stock?threshold={n}**: Listar libros con stock menor al umbral indicado (por defecto 10).
- **POST /api/books/{id}/calculate-price/**: Calcular el precio de venta sugerido usando tasa de cambio actual y margen de ganancia.