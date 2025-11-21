import pytest
from src.modules.rooms.room_service import RoomService


class TestRoomService:
    """Pruebas unitarias para el servicio de salas."""
    
    def test_create_room_success(self, test_db):
        """
        Test 1: Crear una sala válida debe funcionar correctamente.
        
        Verifica:
        - La sala se crea con los datos correctos
        - Por defecto está activa
        """
        service = RoomService(test_db)
        
        room = service.create_room(
            nombre="Sala A1",
            capacidad=10,
            ubicacion="Edificio Principal"
        )
        
        assert room.id is not None
        assert room.nombre == "Sala A1"
        assert room.capacidad == 10
        assert room.ubicacion == "Edificio Principal"
        assert room.activa is True
    
    def test_create_room_invalid_capacity(self, test_db):
        """
        Test 2: No se debe permitir crear salas con capacidad menor a 1.
        
        Verifica:
        - Lanza ValueError si la capacidad es 0 o negativa
        """
        service = RoomService(test_db)
        
        with pytest.raises(ValueError) as exc_info:
            service.create_room(
                nombre="Sala Inválida",
                capacidad=0,
                ubicacion="Algún lugar"
            )
        
        assert "capacidad debe ser al menos 1" in str(exc_info.value)
    
    def test_update_room_success(self, test_db):
        """
        Test 3: Actualizar una sala debe modificar sus datos correctamente.
        
        Verifica:
        - Los datos se actualizan correctamente
        - Se puede cambiar el estado activo/inactivo
        """
        service = RoomService(test_db)
        
        # Crear sala
        room = service.create_room(
            nombre="Sala Original",
            capacidad=5,
            ubicacion="Piso 1"
        )
        
        # Actualizar sala
        updated_room = service.update_room(
            room_id=room.id,
            nombre="Sala Actualizada",
            capacidad=15,
            ubicacion="Piso 2",
            activa=False
        )
        
        assert updated_room.nombre == "Sala Actualizada"
        assert updated_room.capacidad == 15
        assert updated_room.ubicacion == "Piso 2"
        assert updated_room.activa is False
    
    def test_delete_room_without_reservations(self, test_db):
        """
        Test 4: Se debe poder eliminar una sala sin reservas.
        
        Verifica:
        - La sala se elimina exitosamente
        - No se puede consultar después de eliminar
        """
        service = RoomService(test_db)
        
        # Crear sala
        room = service.create_room(
            nombre="Sala Temporal",
            capacidad=8,
            ubicacion="Piso 3"
        )
        
        # Eliminar sala (sin reservas)
        service.delete_room(room.id)
        
        # Verificar que ya no existe
        with pytest.raises(ValueError):
            service.get_room_by_id(room.id)
