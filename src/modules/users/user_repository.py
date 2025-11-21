from typing import List, Optional
from sqlalchemy.orm import Session
from src.modules.users.user_model import User


class UserRepository:
    """
    Repositorio de Usuarios.
    
    Maneja todas las operaciones de acceso a datos (CRUD básico).
    No contiene lógica de negocio, solo consultas a BD.
    """
    
    def __init__(self, db: Session):
        """
        Args:
            db: Sesión de SQLAlchemy
        """
        self.db = db
    
    def create(self, nombre: str, email: str) -> User:
        """
        Crea un nuevo usuario en la base de datos.
        
        Args:
            nombre: Nombre del usuario
            email: Email del usuario
            
        Returns:
            Usuario creado con su ID asignado
        """
        user = User(nombre=nombre, email=email)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Busca un usuario por su ID.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Usuario encontrado o None
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Busca un usuario por su email.
        
        Args:
            email: Email del usuario
            
        Returns:
            Usuario encontrado o None
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_all(self) -> List[User]:
        """
        Retorna todos los usuarios.
        
        Returns:
            Lista de todos los usuarios
        """
        return self.db.query(User).all()
