import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
import os

# IMPORTANTE: Importar modelos ANTES de importar app
# Esto asegura que los modelos estén registrados en Base.metadata
from src.shared.database.connection import Base, get_db
from src.modules.users.user_model import User
from src.modules.rooms.room_model import Room
from src.modules.reservations.reservation_model import Reservation

# Ahora importar la app
from api import app


# Crear base de datos de prueba EN ARCHIVO TEMPORAL
# SQLite en memoria tiene problemas con TestClient porque usa diferentes hilos
TEST_DB_FILE = "test_database.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///./{TEST_DB_FILE}"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=False  # Desactivar logs SQL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Override de la dependencia de BD para usar BD de prueba."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Configurar la app para usar BD de prueba ANTES de cualquier test
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def test_client():
    """
    Fixture que crea un cliente de prueba para hacer requests HTTP.
    Se crea una base de datos limpia para cada test.
    """
    # Eliminar archivo de BD si existe
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)
    
    # Crear todas las tablas frescas
    Base.metadata.create_all(bind=test_engine)
    
    # Crear cliente de prueba
    client = TestClient(app)
    
    yield client
    
    # Limpiar: cerrar conexiones y eliminar archivo
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)


class TestIntegration:
    """
    Pruebas de integración end-to-end.
    
    Simula el flujo completo de un usuario real:
    1. Crear usuarios
    2. Crear salas
    3. Crear reservas
    4. Consultar disponibilidad (con caché)
    """
    
    def test_complete_booking_flow(self, test_client):
        """
        Test de integración: Flujo completo de reserva.
        
        Simula el caso de uso completo:
        1. Registrar dos usuarios
        2. Crear una sala
        3. Primera reserva exitosa
        4. Segunda reserva que se solapa (debe fallar)
        5. Consultar disponibilidad
        6. Verificar que las reservas están guardadas
        """
        
        # === PASO 1: Crear usuarios ===
        
        user1_response = test_client.post("/users/", json={
            "nombre": "Juan Pérez",
            "email": "juan@example.com"
        })
        assert user1_response.status_code == 201
        user1 = user1_response.json()
        assert user1["nombre"] == "Juan Pérez"
        
        user2_response = test_client.post("/users/", json={
            "nombre": "María García",
            "email": "maria@example.com"
        })
        assert user2_response.status_code == 201
        user2 = user2_response.json()
        
        # === PASO 2: Crear sala ===
        
        room_response = test_client.post("/rooms/", json={
            "nombre": "Sala Coworking A1",
            "capacidad": 10,
            "ubicacion": "Edificio Principal, Piso 2"
        })
        assert room_response.status_code == 201
        room = room_response.json()
        assert room["activa"] is True
        
        # === PASO 3: Crear primera reserva (debe funcionar) ===
        
        reservation1_response = test_client.post("/reservations/", json={
            "userId": user1["id"],
            "roomId": room["id"],
            "date": "2025-12-15",
            "startHour": 10,
            "endHour": 12
        })
        assert reservation1_response.status_code == 201
        reservation1 = reservation1_response.json()
        assert reservation1["start_hour"] == 10
        assert reservation1["end_hour"] == 12
        
        # === PASO 4: Intentar reserva solapada (debe fallar) ===
        
        reservation2_response = test_client.post("/reservations/", json={
            "userId": user2["id"],
            "roomId": room["id"],
            "date": "2025-12-15",
            "startHour": 11,  # Se solapa con 10-12
            "endHour": 13
        })
        assert reservation2_response.status_code == 400
        assert "Ya existe una reserva" in reservation2_response.json()["detail"]
        
        # === PASO 5: Crear reserva en horario diferente (debe funcionar) ===
        
        reservation3_response = test_client.post("/reservations/", json={
            "userId": user2["id"],
            "roomId": room["id"],
            "date": "2025-12-15",
            "startHour": 14,  # No se solapa
            "endHour": 16
        })
        assert reservation3_response.status_code == 201
        
        # === PASO 6: Consultar disponibilidad (usa caché) ===
        
        availability_response = test_client.get(
            f"/rooms/{room['id']}/availability",
            params={"date": "2025-12-15"}
        )
        assert availability_response.status_code == 200
        availability = availability_response.json()
        
        # Verificar que los slots ocupados (10, 11, 14, 15) no están disponibles
        free_slots = availability["freeSlots"]
        assert 10 not in free_slots  # Ocupado por reserva 1
        assert 11 not in free_slots  # Ocupado por reserva 1
        assert 14 not in free_slots  # Ocupado por reserva 3
        assert 15 not in free_slots  # Ocupado por reserva 3
        
        # Verificar que otros slots están disponibles
        assert 8 in free_slots
        assert 9 in free_slots
        assert 12 in free_slots
        assert 13 in free_slots
        
        # === PASO 7: Consultar reservas de la sala ===
        
        room_reservations_response = test_client.get(f"/reservations/room/{room['id']}")
        assert room_reservations_response.status_code == 200
        reservations = room_reservations_response.json()
        assert len(reservations) == 2  # Solo 2 reservas exitosas
        
        # === PASO 8: Intentar eliminar sala con reservas futuras (debe fallar) ===
        
        delete_response = test_client.delete(f"/rooms/{room['id']}")
        assert delete_response.status_code == 400
        assert "reserva(s) futura(s)" in delete_response.json()["detail"]
        
        # === PASO 9: Desactivar sala ===
        
        update_response = test_client.put(f"/rooms/{room['id']}", json={
            "nombre": room["nombre"],
            "capacidad": room["capacidad"],
            "ubicacion": room["ubicacion"],
            "activa": False
        })
        assert update_response.status_code == 200
        updated_room = update_response.json()
        assert updated_room["activa"] is False
        
        # === PASO 10: Intentar reservar sala inactiva (debe fallar) ===
        
        reservation4_response = test_client.post("/reservations/", json={
            "userId": user1["id"],
            "roomId": room["id"],
            "date": "2025-12-20",
            "startHour": 9,
            "endHour": 11
        })
        assert reservation4_response.status_code == 400
        assert "no está activa" in reservation4_response.json()["detail"]
    
    def test_user_email_uniqueness(self, test_client):
        """
        Test de integración: Verificar que el email debe ser único.
        """
        # Crear primer usuario
        test_client.post("/users/", json={
            "nombre": "Carlos López",
            "email": "carlos@example.com"
        })
        
        # Intentar crear segundo usuario con mismo email
        duplicate_response = test_client.post("/users/", json={
            "nombre": "Carlos Duplicado",
            "email": "carlos@example.com"
        })
        
        assert duplicate_response.status_code == 400
        assert "Ya existe un usuario" in duplicate_response.json()["detail"]
    
    def test_room_capacity_validation(self, test_client):
        """
        Test de integración: Verificar validación de capacidad mínima.
        """
        invalid_room_response = test_client.post("/rooms/", json={
            "nombre": "Sala Inválida",
            "capacidad": 0,  # Inválido
            "ubicacion": "Algún lugar"
        })
        
        # Pydantic devuelve 422 para errores de validación
        assert invalid_room_response.status_code == 422
        # Verificar que el error menciona el problema de capacidad
        errors = invalid_room_response.json()["detail"]
        assert any("capacidad" in str(error).lower() for error in errors)
