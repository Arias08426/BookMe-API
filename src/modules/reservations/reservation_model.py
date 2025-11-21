from sqlalchemy import Column, Date, ForeignKey, Integer

from src.shared.database.connection import Base


class Reservation(Base):
    """
    Modelo de Reserva.

    Representa una reserva de una sala por un usuario en un rango de horas.

    Atributos:
        id: Identificador único
        user_id: ID del usuario que hace la reserva
        room_id: ID de la sala reservada
        date: Fecha de la reserva
        start_hour: Hora de inicio (0-23)
        end_hour: Hora de fin (0-23)
    """

    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    start_hour = Column(Integer, nullable=False)
    end_hour = Column(Integer, nullable=False)

    def __repr__(self):
        return (
            f"<Reservation(id={self.id}, user_id={self.user_id}, room_id={self.room_id}, "
            f"date={self.date}, {self.start_hour}-{self.end_hour})>"
        )
