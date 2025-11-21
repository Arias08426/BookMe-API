from sqlalchemy import Column, Integer, String

from src.shared.database.connection import Base


class User(Base):
    """
    Modelo de Usuario.

    Representa a los usuarios que pueden realizar reservas.

    Atributos:
        id: Identificador único
        nombre: Nombre completo del usuario
        email: Correo electrónico (único)
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)

    def __repr__(self):
        return f"<User(id={self.id}, nombre='{self.nombre}', email='{self.email}')>"
