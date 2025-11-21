# BookMe API

Sistema de gestión de reservas para salas (coworking, consultorios, salas de estudio).

## 📋 Descripción

BookMe API es un backend REST que permite:
- Gestionar salas (CRUD completo)
- Registrar usuarios
- Crear y consultar reservas
- Cachear disponibilidad de salas para optimizar rendimiento

## 🚀 Características

- ✅ API REST con FastAPI
- ✅ Arquitectura modular (rooms, users, reservations)
- ✅ Lógica de negocio en servicios
- ✅ Validaciones robustas (no solapamiento de reservas)
- ✅ Sistema de caché para disponibilidad
- ✅ Pruebas unitarias e integración
- ✅ Base de datos SQLite (fácil de cambiar a PostgreSQL/MySQL)

## 📁 Estructura del Proyecto

```
BookMe API/
├── src/
│   ├── modules/
│   │   ├── rooms/          # Módulo de salas
│   │   ├── users/          # Módulo de usuarios
│   │   └── reservations/   # Módulo de reservas
│   └── shared/
│       ├── cache/          # Sistema de caché
│       ├── database/       # Conexión a BD
│       └── config/         # Configuración
├── tests/
│   ├── unit/              # Pruebas unitarias
│   └── integration/       # Pruebas de integración
├── api.py                 # Punto de entrada
└── requirements.txt
```

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repo>
cd "BookMe API"
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
```

### 5. Iniciar el servidor
```bash
python api.py
```

La API estará disponible en: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

## 📡 Endpoints Principales

### Salas (Rooms)
- `GET /rooms` - Listar todas las salas
- `POST /rooms` - Crear una sala
- `GET /rooms/{id}` - Obtener sala por ID
- `PUT /rooms/{id}` - Actualizar sala
- `DELETE /rooms/{id}` - Eliminar sala
- `GET /rooms/{id}/availability?date=YYYY-MM-DD` - Ver disponibilidad

### Usuarios (Users)
- `GET /users` - Listar usuarios
- `POST /users` - Crear usuario
- `GET /users/{id}` - Obtener usuario

### Reservas (Reservations)
- `POST /reservations` - Crear reserva
- `GET /reservations/{id}` - Obtener reserva
- `GET /rooms/{id}/reservations` - Reservas de una sala

### Ejemplo de Reserva

```json
POST /reservations
{
  "userId": 1,
  "roomId": 5,
  "date": "2025-02-19",
  "startHour": 10,
  "endHour": 12
}
```

## 🧪 Pruebas

Ejecutar todas las pruebas:
```bash
pytest
```

Ejecutar con cobertura:
```bash
pytest --cov=src tests/
```

## 🏗️ Arquitectura

### Capas por Módulo

1. **Model**: Define la estructura de datos (SQLAlchemy)
2. **Repository**: Acceso a datos (CRUD básico)
3. **Service**: Lógica de negocio y validaciones
4. **Controller**: Maneja requests/responses
5. **Routes**: Define los endpoints

### Sistema de Caché

El caché almacena la disponibilidad de cada sala por día:
- Clave: `availability:roomId:date`
- Se invalida al crear/eliminar reservas
- Implementado en memoria (puede cambiar a Redis)

## 📝 Reglas de Negocio

### Salas
- Capacidad mínima: 1 persona
- No se pueden eliminar salas con reservas futuras
- Solo salas activas pueden ser reservadas

### Reservas
- `startHour` debe ser menor que `endHour`
- No se permiten reservas solapadas
- Usuario y sala deben existir
- Solo salas activas son reservables

## 🔧 Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **Pydantic**: Validación de datos
- **Pytest**: Framework de testing
- **Redis** (opcional): Sistema de caché distribuido

## 👨‍💻 Desarrollo

El proyecto está diseñado con:
- Código limpio y modular
- Separación de responsabilidades
- Fácil mantenimiento y escalabilidad
- Preparado para agregar autenticación JWT
- Listo para Docker y CI/CD

## 📄 Licencia

MIT License
