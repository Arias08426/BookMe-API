from typing import List, Optional
from sqlalchemy.orm import Session
from src.modules.rooms.room_model import Room


class RoomRepository:
    """
    Repositorio de Salas.
    
    Maneja todas las operaciones de acceso a datos para salas.
    """
    
    def __init__(self, db: Session):
        """
        Args:
            db: Sesión de SQLAlchemy
        """
        self.db = db
    
    def create(self, nombre: str, capacidad: int, ubicacion: str, activa: bool = True) -> Room:
        """
        Crea una nueva sala.
        
        Args:
            nombre: Nombre de la sala
            capacidad: Capacidad de personas
            ubicacion: Ubicación física
            activa: Estado inicial (por defecto True)
            
        Returns:
            Sala creada con su ID asignado
        """
        room = Room(
            nombre=nombre,
            capacidad=capacidad,
            ubicacion=ubicacion,
            activa=activa
        )
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room
    
    def get_by_id(self, room_id: int) -> Optional[Room]:
        """
        Busca una sala por su ID.
        
        Args:
            room_id: ID de la sala
            
        Returns:
            Sala encontrada o None
        """
        return self.db.query(Room).filter(Room.id == room_id).first()
    
    def get_all(self) -> List[Room]:
        """
        Retorna todas las salas.
        
        Returns:
            Lista de todas las salas
        """
        return self.db.query(Room).all()
    
    def update(self, room: Room) -> Room:
        """
        Actualiza una sala existente.
        
        Args:
            room: Sala con los datos modificados
            
        Returns:
            Sala actualizada
        """
        self.db.commit()
        self.db.refresh(room)
        return room
    
    def delete(self, room: Room) -> None:
        """
        Elimina una sala.
        
        Args:
            room: Sala a eliminar
        """
        self.db.delete(room)
        self.db.commit()
