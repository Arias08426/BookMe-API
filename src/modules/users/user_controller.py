from pydantic import BaseModel, Field, EmailStr
from typing import List


# Schemas de entrada (request)

class UserCreateRequest(BaseModel):
    """
    Esquema para crear un usuario.
    Define qué datos se esperan en el POST.
    """
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Email único del usuario")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Juan Pérez",
                    "email": "juan.perez@example.com"
                }
            ]
        }
    }


# Schemas de salida (response)

class UserResponse(BaseModel):
    """
    Esquema de respuesta de un usuario.
    Define qué datos se devuelven al cliente.
    """
    id: int
    nombre: str
    email: str
    
    model_config = {
        "from_attributes": True  # Permite convertir desde modelos SQLAlchemy
    }


# Controller

class UserController:
    """
    Controlador de Usuarios.
    
    Maneja las peticiones HTTP y respuestas:
    - Valida entrada con Pydantic
    - Llama al servicio
    - Formatea la respuesta
    """
    
    def __init__(self, service):
        """
        Args:
            service: Instancia de UserService
        """
        self.service = service
    
    def create_user(self, request: UserCreateRequest) -> UserResponse:
        """
        Crea un nuevo usuario.
        
        Args:
            request: Datos del usuario a crear
            
        Returns:
            Usuario creado
        """
        user = self.service.create_user(
            nombre=request.nombre,
            email=request.email
        )
        return UserResponse.model_validate(user)
    
    def get_user(self, user_id: int) -> UserResponse:
        """
        Obtiene un usuario por ID.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Usuario encontrado
        """
        user = self.service.get_user_by_id(user_id)
        return UserResponse.model_validate(user)
    
    def get_all_users(self) -> List[UserResponse]:
        """
        Obtiene todos los usuarios.
        
        Returns:
            Lista de usuarios
        """
        users = self.service.get_all_users()
        return [UserResponse.model_validate(user) for user in users]
