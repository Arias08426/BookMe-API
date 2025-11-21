from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.modules.rooms.room_controller import (AvailabilityResponse,
                                               RoomController,
                                               RoomCreateRequest, RoomResponse,
                                               RoomUpdateRequest)
from src.modules.rooms.room_service import RoomService
from src.shared.database.connection import get_db

# Router de salas
router = APIRouter(prefix="/rooms", tags=["rooms"])


def get_controller(db: Session = Depends(get_db)) -> RoomController:
    """Inyección de dependencias para el controlador."""
    service = RoomService(db)
    return RoomController(service)


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(
    request: RoomCreateRequest, controller: RoomController = Depends(get_controller)
):
    """
    Crea una nueva sala.

    - **nombre**: Nombre de la sala
    - **capacidad**: Número de personas (mínimo 1)
    - **ubicacion**: Ubicación física
    """
    try:
        return controller.create_room(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, controller: RoomController = Depends(get_controller)):
    """
    Obtiene una sala por su ID.
    """
    try:
        return controller.get_room(room_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/", response_model=List[RoomResponse])
def get_all_rooms(controller: RoomController = Depends(get_controller)):
    """
    Lista todas las salas.
    """
    return controller.get_all_rooms()


@router.put("/{room_id}", response_model=RoomResponse)
def update_room(
    room_id: int,
    request: RoomUpdateRequest,
    controller: RoomController = Depends(get_controller),
):
    """
    Actualiza una sala existente.

    Permite modificar todos los campos incluido el estado (activa/inactiva).
    """
    try:
        return controller.update_room(room_id, request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{room_id}", status_code=status.HTTP_200_OK)
def delete_room(room_id: int, controller: RoomController = Depends(get_controller)):
    """
    Elimina una sala.

    **Regla**: No se puede eliminar una sala con reservas futuras.
    """
    try:
        return controller.delete_room(room_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{room_id}/availability", response_model=AvailabilityResponse)
def get_room_availability(
    room_id: int,
    date: str = Query(..., description="Fecha en formato YYYY-MM-DD"),
    controller: RoomController = Depends(get_controller),
):
    """
    Obtiene la disponibilidad de una sala en una fecha específica.

    Retorna las horas libres (slots) disponibles para reservar.
    Utiliza caché para optimizar consultas repetidas.

    - **date**: Fecha en formato YYYY-MM-DD (ej: 2025-02-19)
    """
    try:
        return controller.get_availability(room_id, date)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
