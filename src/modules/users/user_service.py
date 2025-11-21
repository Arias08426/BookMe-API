from typing import List

from sqlalchemy.orm import Session

from src.modules.users.user_model import User
from src.modules.users.user_repository import UserRepository


class UserService:
    """
    Servicio de Usuarios.

    Contiene la lógica de negocio:
    - Validaciones
    - Reglas de negocio
    - Coordinación entre repositorios
    """

    def __init__(self, db: Session):
        """
        Args:
            db: Sesión de SQLAlchemy
        """
        self.repository = UserRepository(db)

    def create_user(self, nombre: str, email: str) -> User:
        """
        Crea un nuevo usuario con validaciones.

        Reglas:
        - El email no puede estar duplicado
        - El nombre no puede estar vacío

        Args:
            nombre: Nombre del usuario
            email: Email del usuario

        Returns:
            Usuario creado

        Raises:
            ValueError: Si las validaciones fallan
        """
        # Validar que el nombre no esté vacío
        if not nombre or nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacío")

        # Validar que el email no esté vacío
        if not email or email.strip() == "":
            raise ValueError("El email no puede estar vacío")

        # Validar formato básico de email
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("El email no tiene un formato válido")

        # Validar que el email no esté duplicado
        existing_user = self.repository.get_by_email(email)
        if existing_user:
            raise ValueError(f"Ya existe un usuario con el email '{email}'")

        return self.repository.create(nombre=nombre, email=email)

    def get_user_by_id(self, user_id: int) -> User:
        """
        Obtiene un usuario por ID.

        Args:
            user_id: ID del usuario

        Returns:
            Usuario encontrado

        Raises:
            ValueError: Si el usuario no existe
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"No se encontró el usuario con ID {user_id}")
        return user

    def get_all_users(self) -> List[User]:
        """
        Retorna todos los usuarios.

        Returns:
            Lista de usuarios
        """
        return self.repository.get_all()
