from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.shared.database.connection import get_db
from src.modules.users.user_service import UserService
from src.modules.users.user_controller import UserController, UserCreateRequest, UserResponse

# Router de usuarios
router = APIRouter(
    prefix="/users",
    tags=["users"]
)


def get_controller(db: Session = Depends(get_db)) -> UserController:
    """Inyección de dependencias para el controlador."""
    service = UserService(db)
    return UserController(service)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    request: UserCreateRequest,
    controller: UserController = Depends(get_controller)
):
    """
    Crea un nuevo usuario.
    
    - **nombre**: Nombre completo del usuario
    - **email**: Email único (no puede estar duplicado)
    """
    try:
        return controller.create_user(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    controller: UserController = Depends(get_controller)
):
    """
    Obtiene un usuario por su ID.
    """
    try:
        return controller.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/", response_model=List[UserResponse])
def get_all_users(
    controller: UserController = Depends(get_controller)
):
    """
    Lista todos los usuarios registrados.
    """
    return controller.get_all_users()
