from typing import List
from sqlalchemy.orm import Session
from datetime import date
from src.modules.reservations.reservation_model import Reservation
from src.modules.reservations.reservation_repository import ReservationRepository
from src.modules.users.user_repository import UserRepository
from src.modules.rooms.room_repository import RoomRepository
from src.shared.cache.cache_service import get_cache


class ReservationService:
    """
    Servicio de Reservas.
    
    Contiene toda la lógica de negocio para reservas:
    - Validaciones complejas
    - Detección de solapamientos
    - Invalidación de caché
    """
    
    def __init__(self, db: Session):
        """
        Args:
            db: Sesión de SQLAlchemy
        """
        self.repository = ReservationRepository(db)
        self.user_repository = UserRepository(db)
        self.room_repository = RoomRepository(db)
        self.cache = get_cache()
    
    def create_reservation(self, user_id: int, room_id: int, reservation_date: date,
                          start_hour: int, end_hour: int) -> Reservation:
        """
        Crea una nueva reserva con todas las validaciones.
        
        Reglas:
        1. startHour < endHour
        2. El usuario debe existir
        3. La sala debe existir y estar activa
        4. No debe haber solapamiento con otras reservas
        
        Args:
            user_id: ID del usuario
            room_id: ID de la sala
            reservation_date: Fecha de la reserva
            start_hour: Hora de inicio (0-23)
            end_hour: Hora de fin (0-23)
            
        Returns:
            Reserva creada
            
        Raises:
            ValueError: Si alguna validación falla
        """
        # Validación 1: startHour < endHour
        if start_hour >= end_hour:
            raise ValueError("La hora de inicio debe ser menor que la hora de fin")
        
        # Validar rango de horas válido
        if not (0 <= start_hour <= 23) or not (0 <= end_hour <= 23):
            raise ValueError("Las horas deben estar entre 0 y 23")
        
        # Validación 2: El usuario debe existir
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"No existe el usuario con ID {user_id}")
        
        # Validación 3: La sala debe existir
        room = self.room_repository.get_by_id(room_id)
        if not room:
            raise ValueError(f"No existe la sala con ID {room_id}")
        
        # Validación 3b: La sala debe estar activa
        if not room.activa:
            raise ValueError("La sala no está activa y no puede ser reservada")
        
        # Validación 4: No debe haber solapamiento
        has_overlap = self.repository.check_overlap(
            room_id=room_id,
            reservation_date=reservation_date,
            start_hour=start_hour,
            end_hour=end_hour
        )
        
        if has_overlap:
            raise ValueError(
                f"Ya existe una reserva en ese horario. "
                f"La sala {room_id} no está disponible de {start_hour} a {end_hour}"
            )
        
        # Crear la reserva
        reservation = self.repository.create(
            user_id=user_id,
            room_id=room_id,
            reservation_date=reservation_date,
            start_hour=start_hour,
            end_hour=end_hour
        )
        
        # Invalidar caché de disponibilidad
        self._invalidate_availability_cache(room_id, reservation_date)
        
        return reservation
    
    def get_reservation_by_id(self, reservation_id: int) -> Reservation:
        """
        Obtiene una reserva por ID.
        
        Args:
            reservation_id: ID de la reserva
            
        Returns:
            Reserva encontrada
            
        Raises:
            ValueError: Si la reserva no existe
        """
        reservation = self.repository.get_by_id(reservation_id)
        if not reservation:
            raise ValueError(f"No se encontró la reserva con ID {reservation_id}")
        return reservation
    
    def get_reservations_by_room(self, room_id: int) -> List[Reservation]:
        """
        Obtiene todas las reservas de una sala.
        
        Args:
            room_id: ID de la sala
            
        Returns:
            Lista de reservas
            
        Raises:
            ValueError: Si la sala no existe
        """
        # Verificar que la sala exista
        room = self.room_repository.get_by_id(room_id)
        if not room:
            raise ValueError(f"No existe la sala con ID {room_id}")
        
        return self.repository.get_by_room(room_id)
    
    def _invalidate_availability_cache(self, room_id: int, reservation_date: date) -> None:
        """
        Invalida el caché de disponibilidad para una sala y fecha.
        
        Args:
            room_id: ID de la sala
            reservation_date: Fecha de la reserva
        """
        cache_key = self.cache.get_cache_key("availability", str(room_id), str(reservation_date))
        self.cache.delete(cache_key)
