from datetime import date
from typing import List

from sqlalchemy.orm import Session

from src.modules.rooms.room_model import Room
from src.modules.rooms.room_repository import RoomRepository
from src.shared.cache.cache_service import get_cache


class RoomService:
    """
    Servicio de Salas.

    Contiene la lógica de negocio para la gestión de salas.
    """

    def __init__(self, db: Session):
        """
        Args:
            db: Sesión de SQLAlchemy
        """
        self.repository = RoomRepository(db)
        self.cache = get_cache()
        self.db = db

    def create_room(self, nombre: str, capacidad: int, ubicacion: str) -> Room:
        """
        Crea una nueva sala con validaciones.

        Reglas:
        - La capacidad debe ser >= 1
        - El nombre no puede estar vacío

        Args:
            nombre: Nombre de la sala
            capacidad: Capacidad de personas
            ubicacion: Ubicación física

        Returns:
            Sala creada

        Raises:
            ValueError: Si las validaciones fallan
        """
        # Validar nombre
        if not nombre or nombre.strip() == "":
            raise ValueError("El nombre de la sala no puede estar vacío")

        # Validar capacidad
        if capacidad < 1:
            raise ValueError("La capacidad debe ser al menos 1 persona")

        # Validar ubicación
        if not ubicacion or ubicacion.strip() == "":
            raise ValueError("La ubicación no puede estar vacía")

        return self.repository.create(
            nombre=nombre, capacidad=capacidad, ubicacion=ubicacion
        )

    def get_room_by_id(self, room_id: int) -> Room:
        """
        Obtiene una sala por ID.

        Args:
            room_id: ID de la sala

        Returns:
            Sala encontrada

        Raises:
            ValueError: Si la sala no existe
        """
        room = self.repository.get_by_id(room_id)
        if not room:
            raise ValueError(f"No se encontró la sala con ID {room_id}")
        return room

    def get_all_rooms(self) -> List[Room]:
        """
        Retorna todas las salas.

        Returns:
            Lista de salas
        """
        return self.repository.get_all()

    def update_room(
        self, room_id: int, nombre: str, capacidad: int, ubicacion: str, activa: bool
    ) -> Room:
        """
        Actualiza una sala existente.

        Args:
            room_id: ID de la sala
            nombre: Nuevo nombre
            capacidad: Nueva capacidad
            ubicacion: Nueva ubicación
            activa: Nuevo estado

        Returns:
            Sala actualizada

        Raises:
            ValueError: Si las validaciones fallan
        """
        # Obtener la sala
        room = self.get_room_by_id(room_id)

        # Validaciones
        if not nombre or nombre.strip() == "":
            raise ValueError("El nombre de la sala no puede estar vacío")

        if capacidad < 1:
            raise ValueError("La capacidad debe ser al menos 1 persona")

        if not ubicacion or ubicacion.strip() == "":
            raise ValueError("La ubicación no puede estar vacía")

        # Actualizar campos
        room.nombre = nombre
        room.capacidad = capacidad
        room.ubicacion = ubicacion
        room.activa = activa

        return self.repository.update(room)

    def delete_room(self, room_id: int) -> None:
        """
        Elimina una sala.

        Regla:
        - No se puede eliminar una sala con reservas futuras

        Args:
            room_id: ID de la sala

        Raises:
            ValueError: Si la sala tiene reservas futuras
        """
        from datetime import date

        from src.modules.reservations.reservation_model import Reservation

        room = self.get_room_by_id(room_id)

        # Verificar si tiene reservas futuras
        future_reservations = (
            self.db.query(Reservation)
            .filter(Reservation.room_id == room_id, Reservation.date >= date.today())
            .count()
        )

        if future_reservations > 0:
            raise ValueError(
                f"No se puede eliminar la sala porque tiene {future_reservations} reserva(s) futura(s)"
            )

        self.repository.delete(room)

    def get_availability(self, room_id: int, target_date: date) -> dict:
        """
        Obtiene la disponibilidad de una sala en una fecha.

        Utiliza caché para optimizar consultas repetidas.

        Args:
            room_id: ID de la sala
            target_date: Fecha a consultar

        Returns:
            Dict con roomId, date, freeSlots
        """
        from src.modules.reservations.reservation_model import Reservation

        # Verificar caché
        cache_key = self.cache.get_cache_key(
            "availability", str(room_id), str(target_date)
        )
        cached_data = self.cache.get(cache_key)

        if cached_data:
            return cached_data

        # Verificar que la sala existe y está activa
        room = self.get_room_by_id(room_id)
        if not room.activa:
            raise ValueError("La sala no está activa")

        # Obtener reservas de ese día
        reservations = (
            self.db.query(Reservation)
            .filter(Reservation.room_id == room_id, Reservation.date == target_date)
            .all()
        )

        # Calcular slots ocupados
        occupied_hours = set()
        for reservation in reservations:
            for hour in range(reservation.start_hour, reservation.end_hour):
                occupied_hours.add(hour)

        # Slots disponibles (asumimos horario de 8 a 20)
        all_hours = set(range(8, 20))
        free_slots = sorted(list(all_hours - occupied_hours))

        # Preparar resultado
        result = {"roomId": room_id, "date": str(target_date), "freeSlots": free_slots}

        # Guardar en caché
        self.cache.set(cache_key, result)

        return result
