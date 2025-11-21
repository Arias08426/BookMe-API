from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.shared.database.connection import init_db
from src.shared.config.settings import get_settings
from src.modules.users.user_routes import router as user_router
from src.modules.rooms.room_routes import router as room_router
from src.modules.reservations.reservation_routes import router as reservation_router

# Configuración
settings = get_settings()

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    API REST para gestión de reservas de salas.
    
    ## Características
    
    * **Usuarios**: Registro y consulta de usuarios
    * **Salas**: CRUD completo de salas con control de estado
    * **Reservas**: Creación de reservas con validación de solapamiento
    * **Caché**: Sistema de caché para consultas de disponibilidad
    
    ## Reglas de Negocio
    
    ### Salas
    - Capacidad mínima: 1 persona
    - No se pueden eliminar salas con reservas futuras
    - Solo salas activas pueden ser reservadas
    
    ### Reservas
    - startHour < endHour
    - Usuario y sala deben existir
    - Solo salas activas son reservables
    - No se permiten reservas solapadas
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS (permitir peticiones desde el frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers (endpoints)
app.include_router(user_router)
app.include_router(room_router)
app.include_router(reservation_router)


@app.on_event("startup")
def on_startup():
    """
    Se ejecuta al iniciar la aplicación.
    Crea las tablas en la base de datos si no existen.
    """
    print(f"🚀 Iniciando {settings.app_name} v{settings.app_version}")
    print("📊 Inicializando base de datos...")
    init_db()
    print("✅ Base de datos inicializada correctamente")
    print(f"📡 Documentación disponible en: http://localhost:8000/docs")


@app.get("/", tags=["health"])
def root():
    """
    Endpoint raíz para verificar que la API está funcionando.
    """
    return {
        "message": f"Bienvenido a {settings.app_name}",
        "version": settings.app_version,
        "status": "online",
        "docs": "/docs"
    }


@app.get("/health", tags=["health"])
def health_check():
    """
    Endpoint de health check para monitoreo.
    """
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version
    }


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 50)
    print(f"  {settings.app_name} - v{settings.app_version}")
    print("=" * 50)
    print()
    
    # Iniciar servidor
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug  # Auto-reload en modo debug
    )
