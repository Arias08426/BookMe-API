from sqlalchemy import Boolean, Column, Integer, String

from src.shared.database.connection import Base


class Room(Base):
    """
    Modelo de Sala.

    Representa una sala que puede ser reservada.

    Atributos:
        id: Identificador único
        nombre: Nombre de la sala
        capacidad: Número de personas que puede albergar
        ubicacion: Ubicación física de la sala
        activa: Si está disponible para reservas (True) o inactiva (False)
    """

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    capacidad = Column(Integer, nullable=False)
    ubicacion = Column(String(200), nullable=False)
    activa = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Room(id={self.id}, nombre='{self.nombre}', capacidad={self.capacidad}, activa={self.activa})>"
