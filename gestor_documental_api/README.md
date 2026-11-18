# Gestor Documental Institucional — API inicial

Repositorio base para desarrollar una API REST en Python/Django con PostgreSQL.
Incluye módulos iniciales para instituciones, identidad institucional, plantillas,
documentos generados, usuarios y auditoría.

## Requisitos
- Windows 10/11
- Python 3.13
- PostgreSQL instalado y servicio iniciado

## 1. Crear la base de datos
En pgAdmin o `psql`, crea una base de datos y un usuario. Ejemplo:

```sql
CREATE USER gestor_user WITH PASSWORD 'CAMBIAR_ESTA_CLAVE';
CREATE DATABASE gestor_documental OWNER gestor_user;
```

## 2. Preparar el entorno en Windows

Abre CMD en la carpeta donde está `manage.py`:

```bat
py -3.13 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
```

Edita `.env` con los datos reales de PostgreSQL. No compartas ese archivo.

## 3. Crear tablas y administrador

```bat
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

La API local queda en `http://127.0.0.1:8000/api/`.
Panel administrativo: `http://127.0.0.1:8000/admin/`
Documentación OpenAPI: `http://127.0.0.1:8000/api/schema/swagger-ui/`
Comprobación: `http://127.0.0.1:8000/api/health/`

## 4. Módulos y endpoints iniciales

- `GET/POST /api/institutions/`
- `GET/POST /api/identities/`
- `GET/POST /api/categories/`
- `GET/POST /api/templates/`
- `GET/POST /api/generated-documents/`
- `GET /api/health/`

Los endpoints requieren autenticación por sesión o token básico de DRF.
Para el primer prototipo se deja habilitada la autenticación de sesión y básica;
antes de usarlo en una red institucional se debe configurar HTTPS, permisos por rol,
copias de seguridad y un servidor WSGI/ASGI de producción. No exponer `runserver`
a Internet ni usarlo como servidor definitivo.

## 5. Plantilla PEI recibida

El archivo `FORMATO PEI(1).docx` se copia en `media/plantillas/` como archivo de
referencia. Se conserva sin alteraciones. El documento tiene múltiples secciones,
tablas y contenido institucional; antes de automatizar su diligenciamiento se hará
un mapeo de campos y pruebas de conservación de formato. No se debe reemplazar
texto de forma global sin validar encabezados, pies, tablas, imágenes y saltos.

## 6. Próximo desarrollo
1. Confirmar campos institucionales comunes y particulares.
2. Crear el módulo de variables/campos del PEI.
3. Implementar generación DOCX con `docxtpl` y pruebas sobre una copia de la plantilla.
4. Añadir permisos granulares, consecutivos y generación por lotes.
