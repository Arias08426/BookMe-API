import pytest
from src.modules.users.user_service import UserService


class TestUserService:
    """Pruebas unitarias para el servicio de usuarios."""
    
    def test_create_user_success(self, test_db):
        """
        Test 1: Crear un usuario válido debe funcionar correctamente.
        
        Verifica:
        - El usuario se crea con un ID asignado
        - Los datos se guardan correctamente
        """
        service = UserService(test_db)
        
        user = service.create_user(
            nombre="Juan Pérez",
            email="juan@example.com"
        )
        
        assert user.id is not None
        assert user.nombre == "Juan Pérez"
        assert user.email == "juan@example.com"
    
    def test_create_user_duplicate_email(self, test_db):
        """
        Test 2: No se debe permitir crear usuarios con email duplicado.
        
        Verifica:
        - El primer usuario se crea exitosamente
        - El segundo con el mismo email lanza ValueError
        """
        service = UserService(test_db)
        
        # Crear primer usuario
        service.create_user(nombre="Juan", email="juan@example.com")
        
        # Intentar crear segundo con mismo email
        with pytest.raises(ValueError) as exc_info:
            service.create_user(nombre="Pedro", email="juan@example.com")
        
        assert "Ya existe un usuario con el email" in str(exc_info.value)
    
    def test_create_user_empty_name(self, test_db):
        """
        Test 3: No se debe permitir crear usuarios con nombre vacío.
        
        Verifica:
        - Lanza ValueError si el nombre está vacío
        """
        service = UserService(test_db)
        
        with pytest.raises(ValueError) as exc_info:
            service.create_user(nombre="", email="test@example.com")
        
        assert "nombre no puede estar vacío" in str(exc_info.value)
    
    def test_get_user_by_id_not_found(self, test_db):
        """
        Test 4: Buscar un usuario que no existe debe lanzar error.
        
        Verifica:
        - Lanza ValueError cuando el ID no existe
        """
        service = UserService(test_db)
        
        with pytest.raises(ValueError) as exc_info:
            service.get_user_by_id(999)
        
        assert "No se encontró el usuario con ID 999" in str(exc_info.value)
