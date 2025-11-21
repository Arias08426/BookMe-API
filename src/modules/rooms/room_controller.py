from typing import List

from pydantic import BaseModel, Field

# Schemas de entrada


class RoomCreateRequest(BaseModel):
    """Esquema para crear una sala."""

    nombre: str = Field(
        ..., min_length=1, max_length=100, description="Nombre de la sala"
    )
    capacidad: int = Field(..., ge=1, description="Capacidad de personas (mínimo 1)")
    ubicacion: str = Field(
        ..., min_length=1, max_length=200, description="Ubicación física"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Sala A1",
                    "capacidad": 10,
                    "ubicacion": "Edificio Principal, Piso 2",
                }
            ]
        }
    }


class RoomUpdateRequest(BaseModel):
    """Esquema para actualizar una sala."""

    nombre: str = Field(..., min_length=1, max_length=100)
    capacidad: int = Field(..., ge=1)
    ubicacion: str = Field(..., min_length=1, max_length=200)
    activa: bool = Field(..., description="Si la sala está disponible para reservas")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "Sala A1 Renovada",
                    "capacidad": 12,
                    "ubicacion": "Edificio Principal, Piso 2",
                    "activa": True,
                }
            ]
        }
    }


# Schemas de salida


class RoomResponse(BaseModel):
    """Esquema de respuesta de una sala."""

    id: int
    nombre: str
    capacidad: int
    ubicacion: str
    activa: bool

    model_config = {"from_attributes": True}


class AvailabilityResponse(BaseModel):
    """Esquema de respuesta de disponibilidad."""

    roomId: int
    date: str
    freeSlots: List[int]


# Controller


class RoomController:
    """
    Controlador de Salas.

    Maneja las peticiones HTTP relacionadas con salas.
    """

    def __init__(self, service):
        """
        Args:
            service: Instancia de RoomService
        """
        self.service = service

    def create_room(self, request: RoomCreateRequest) -> RoomResponse:
        """Crea una nueva sala."""
        room = self.service.create_room(
            nombre=request.nombre,
            capacidad=request.capacidad,
            ubicacion=request.ubicacion,
        )
        return RoomResponse.model_validate(room)

    def get_room(self, room_id: int) -> RoomResponse:
        """Obtiene una sala por ID."""
        room = self.service.get_room_by_id(room_id)
        return RoomResponse.model_validate(room)

    def get_all_rooms(self) -> List[RoomResponse]:
        """Obtiene todas las salas."""
        rooms = self.service.get_all_rooms()
        return [RoomResponse.model_validate(room) for room in rooms]

    def update_room(self, room_id: int, request: RoomUpdateRequest) -> RoomResponse:
        """Actualiza una sala."""
        room = self.service.update_room(
            room_id=room_id,
            nombre=request.nombre,
            capacidad=request.capacidad,
            ubicacion=request.ubicacion,
            activa=request.activa,
        )
        return RoomResponse.model_validate(room)

    def delete_room(self, room_id: int) -> dict:
        """Elimina una sala."""
        self.service.delete_room(room_id)
        return {"message": "Sala eliminada exitosamente"}

    def get_availability(self, room_id: int, target_date: str) -> AvailabilityResponse:
        """Obtiene la disponibilidad de una sala en una fecha."""
        from datetime import datetime

        # Convertir fecha string a date
        try:
            date_obj = datetime.strptime(target_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")

        availability = self.service.get_availability(room_id, date_obj)
        return AvailabilityResponse(**availability)
