from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.modules.reservations.reservation_controller import (
    ReservationController, ReservationCreateRequest, ReservationResponse)
from src.modules.reservations.reservation_service import ReservationService
from src.shared.database.connection import get_db

# Router de reservas
router = APIRouter(prefix="/reservations", tags=["reservations"])


def get_controller(db: Session = Depends(get_db)) -> ReservationController:
    """Inyección de dependencias para el controlador."""
    service = ReservationService(db)
    return ReservationController(service)


@router.post(
    "/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED
)
def create_reservation(
    request: ReservationCreateRequest,
    controller: ReservationController = Depends(get_controller),
):
    """
    Crea una nueva reserva.

    **Reglas de negocio:**
    - startHour debe ser menor que endHour
    - El usuario y la sala deben existir
    - La sala debe estar activa
    - No puede haber solapamiento con otras reservas

    **Body:**
    ```json
    {
      "userId": 1,
      "roomId": 5,
      "date": "2025-02-19",
      "startHour": 10,
      "endHour": 12
    }
    ```
    """
    try:
        return controller.create_reservation(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(
    reservation_id: int, controller: ReservationController = Depends(get_controller)
):
    """
    Obtiene una reserva por su ID.
    """
    try:
        return controller.get_reservation(reservation_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Ruta alternativa para obtener reservas de una sala
# Se podría poner en room_routes.py, pero la dejo aquí por cohesión
@router.get("/room/{room_id}", response_model=List[ReservationResponse])
def get_room_reservations(
    room_id: int, controller: ReservationController = Depends(get_controller)
):
    """
    Obtiene todas las reservas de una sala específica.

    Útil para ver el historial completo de reservas de una sala.
    """
    try:
        return controller.get_reservations_by_room(room_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
