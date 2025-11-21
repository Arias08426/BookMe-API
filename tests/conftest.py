import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.shared.database.connection import Base


@pytest.fixture(scope="function")
def test_db():
    """
    Fixture que crea una base de datos en memoria para tests.
    Se crea y destruye en cada test para aislarlos.
    """
    # Crear engine en memoria
    engine = create_engine("sqlite:///:memory:")
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    # Crear sesión
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    yield session
    
    # Limpiar después del test
    session.close()
