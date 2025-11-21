from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date
from src.modules.reservations.reservation_model import Reservation


class ReservationRepository:
    """
    Repositorio de Reservas.
    
    Maneja todas las operaciones de acceso a datos para reservas.
    """
    
    def __init__(self, db: Session):
        """
        Args:
            db: Sesión de SQLAlchemy
        """
        self.db = db
    
    def create(self, user_id: int, room_id: int, reservation_date: date,
               start_hour: int, end_hour: int) -> Reservation:
        """
        Crea una nueva reserva.
        
        Args:
            user_id: ID del usuario
            room_id: ID de la sala
            reservation_date: Fecha de la reserva
            start_hour: Hora de inicio
            end_hour: Hora de fin
            
        Returns:
            Reserva creada con su ID asignado
        """
        reservation = Reservation(
            user_id=user_id,
            room_id=room_id,
            date=reservation_date,
            start_hour=start_hour,
            end_hour=end_hour
        )
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation
    
    def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        """
        Busca una reserva por su ID.
        
        Args:
            reservation_id: ID de la reserva
            
        Returns:
            Reserva encontrada o None
        """
        return self.db.query(Reservation).filter(Reservation.id == reservation_id).first()
    
    def get_by_room(self, room_id: int) -> List[Reservation]:
        """
        Obtiene todas las reservas de una sala.
        
        Args:
            room_id: ID de la sala
            
        Returns:
            Lista de reservas de la sala
        """
        return self.db.query(Reservation).filter(Reservation.room_id == room_id).all()
    
    def get_by_room_and_date(self, room_id: int, reservation_date: date) -> List[Reservation]:
        """
        Obtiene las reservas de una sala en una fecha específica.
        
        Args:
            room_id: ID de la sala
            reservation_date: Fecha a consultar
            
        Returns:
            Lista de reservas en esa fecha
        """
        return self.db.query(Reservation).filter(
            Reservation.room_id == room_id,
            Reservation.date == reservation_date
        ).all()
    
    def check_overlap(self, room_id: int, reservation_date: date,
                      start_hour: int, end_hour: int) -> bool:
        """
        Verifica si existe solapamiento con otras reservas.
        
        Args:
            room_id: ID de la sala
            reservation_date: Fecha de la reserva
            start_hour: Hora de inicio
            end_hour: Hora de fin
            
        Returns:
            True si hay solapamiento, False si no
        """
        # Obtener reservas del mismo día y sala
        reservations = self.get_by_room_and_date(room_id, reservation_date)
        
        # Verificar solapamiento
        for res in reservations:
            # Dos rangos [A, B) y [C, D) se solapan si:
            # A < D y C < B
            if start_hour < res.end_hour and res.start_hour < end_hour:
                return True
        
        return False
