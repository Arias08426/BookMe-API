from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from src.shared.config.settings import get_settings

# Configuración
settings = get_settings()

# Motor de base de datos
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# Sesión de BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db() -> Session:
    """
    Generador que proporciona una sesión de base de datos.
    Se usa como dependencia en FastAPI.
    
    Ejemplo:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa la base de datos creando todas las tablas.
    Se llama al iniciar la aplicación.
    """
    Base.metadata.create_all(bind=engine)
