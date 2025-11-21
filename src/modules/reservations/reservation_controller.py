from typing import List

from pydantic import BaseModel, Field

# Schemas de entrada


class ReservationCreateRequest(BaseModel):
    """Esquema para crear una reserva."""

    userId: int = Field(..., description="ID del usuario que reserva")
    roomId: int = Field(..., description="ID de la sala a reservar")
    date: str = Field(..., description="Fecha en formato YYYY-MM-DD")
    startHour: int = Field(..., ge=0, le=23, description="Hora de inicio (0-23)")
    endHour: int = Field(..., ge=0, le=23, description="Hora de fin (0-23)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "userId": 1,
                    "roomId": 5,
                    "date": "2025-02-19",
                    "startHour": 10,
                    "endHour": 12,
                }
            ]
        }
    }


# Schemas de salida


class ReservationResponse(BaseModel):
    """Esquema de respuesta de una reserva."""

    id: int
    user_id: int
    room_id: int
    date: str
    start_hour: int
    end_hour: int

    model_config = {"from_attributes": True}

    @classmethod
    def from_model(cls, reservation):
        """Convierte un modelo de reserva a response."""
        return cls(
            id=reservation.id,
            user_id=reservation.user_id,
            room_id=reservation.room_id,
            date=str(reservation.date),
            start_hour=reservation.start_hour,
            end_hour=reservation.end_hour,
        )


# Controller


class ReservationController:
    """
    Controlador de Reservas.

    Maneja las peticiones HTTP relacionadas con reservas.
    """

    def __init__(self, service):
        """
        Args:
            service: Instancia de ReservationService
        """
        self.service = service

    def create_reservation(
        self, request: ReservationCreateRequest
    ) -> ReservationResponse:
        """
        Crea una nueva reserva.

        Args:
            request: Datos de la reserva

        Returns:
            Reserva creada
        """
        from datetime import datetime

        # Convertir fecha string a date
        try:
            date_obj = datetime.strptime(request.date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")

        reservation = self.service.create_reservation(
            user_id=request.userId,
            room_id=request.roomId,
            reservation_date=date_obj,
            start_hour=request.startHour,
            end_hour=request.endHour,
        )

        return ReservationResponse.from_model(reservation)

    def get_reservation(self, reservation_id: int) -> ReservationResponse:
        """
        Obtiene una reserva por ID.

        Args:
            reservation_id: ID de la reserva

        Returns:
            Reserva encontrada
        """
        reservation = self.service.get_reservation_by_id(reservation_id)
        return ReservationResponse.from_model(reservation)

    def get_reservations_by_room(self, room_id: int) -> List[ReservationResponse]:
        """
        Obtiene todas las reservas de una sala.

        Args:
            room_id: ID de la sala

        Returns:
            Lista de reservas
        """
        reservations = self.service.get_reservations_by_room(room_id)
        return [ReservationResponse.from_model(res) for res in reservations]
