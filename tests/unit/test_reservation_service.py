from datetime import date

import pytest

from src.modules.reservations.reservation_service import ReservationService
from src.modules.rooms.room_service import RoomService
from src.modules.users.user_service import UserService


class TestReservationService:
    """Pruebas unitarias para el servicio de reservas."""

    def test_create_reservation_success(self, test_db):
        """
        Test 1: Crear una reserva válida debe funcionar correctamente.

        Verifica:
        - La reserva se crea con todos los datos correctos
        - Se asigna un ID automáticamente
        """
        # Preparar datos: crear usuario y sala
        user_service = UserService(test_db)
        room_service = RoomService(test_db)
        reservation_service = ReservationService(test_db)

        user = user_service.create_user("Ana García", "ana@example.com")
        room = room_service.create_room("Sala Meeting", 6, "Piso 1")

        # Crear reserva
        reservation = reservation_service.create_reservation(
            user_id=user.id,
            room_id=room.id,
            reservation_date=date(2025, 2, 19),
            start_hour=10,
            end_hour=12,
        )

        assert reservation.id is not None
        assert reservation.user_id == user.id
        assert reservation.room_id == room.id
        assert reservation.date == date(2025, 2, 19)
        assert reservation.start_hour == 10
        assert reservation.end_hour == 12

    def test_create_reservation_invalid_hours(self, test_db):
        """
        Test 2: No se debe permitir startHour >= endHour.

        Verifica:
        - Lanza ValueError si las horas son inválidas
        """
        user_service = UserService(test_db)
        room_service = RoomService(test_db)
        reservation_service = ReservationService(test_db)

        user = user_service.create_user("Carlos", "carlos@example.com")
        room = room_service.create_room("Sala B", 4, "Piso 2")

        # Intentar crear con startHour >= endHour
        with pytest.raises(ValueError) as exc_info:
            reservation_service.create_reservation(
                user_id=user.id,
                room_id=room.id,
                reservation_date=date(2025, 3, 15),
                start_hour=14,
                end_hour=14,  # Igual o menor
            )

        assert "hora de inicio debe ser menor" in str(exc_info.value)

    def test_create_reservation_overlap(self, test_db):
        """
        Test 3: No se debe permitir crear reservas que se solapen.

        Verifica:
        - La primera reserva se crea exitosamente
        - La segunda reserva (solapada) lanza ValueError
        """
        user_service = UserService(test_db)
        room_service = RoomService(test_db)
        reservation_service = ReservationService(test_db)

        user1 = user_service.create_user("María", "maria@example.com")
        user2 = user_service.create_user("Pedro", "pedro@example.com")
        room = room_service.create_room("Sala C", 8, "Piso 3")

        # Primera reserva: 10:00 - 12:00
        reservation_service.create_reservation(
            user_id=user1.id,
            room_id=room.id,
            reservation_date=date(2025, 4, 20),
            start_hour=10,
            end_hour=12,
        )

        # Segunda reserva que se solapa: 11:00 - 13:00
        with pytest.raises(ValueError) as exc_info:
            reservation_service.create_reservation(
                user_id=user2.id,
                room_id=room.id,
                reservation_date=date(2025, 4, 20),
                start_hour=11,  # Se solapa con la anterior
                end_hour=13,
            )

        assert "Ya existe una reserva en ese horario" in str(exc_info.value)

    def test_create_reservation_inactive_room(self, test_db):
        """
        Test 4: No se debe permitir reservar salas inactivas.

        Verifica:
        - Lanza ValueError si la sala está inactiva
        """
        user_service = UserService(test_db)
        room_service = RoomService(test_db)
        reservation_service = ReservationService(test_db)

        user = user_service.create_user("Luis", "luis@example.com")
        room = room_service.create_room("Sala Inactiva", 5, "Piso 4")

        # Desactivar la sala
        room_service.update_room(
            room_id=room.id,
            nombre=room.nombre,
            capacidad=room.capacidad,
            ubicacion=room.ubicacion,
            activa=False,
        )

        # Intentar reservar sala inactiva
        with pytest.raises(ValueError) as exc_info:
            reservation_service.create_reservation(
                user_id=user.id,
                room_id=room.id,
                reservation_date=date(2025, 5, 10),
                start_hour=9,
                end_hour=11,
            )

        assert "no está activa" in str(exc_info.value)

    def test_create_reservation_nonexistent_user(self, test_db):
        """
        Test 5: No se debe permitir reservar con un usuario inexistente.

        Verifica:
        - Lanza ValueError si el usuario no existe
        """
        room_service = RoomService(test_db)
        reservation_service = ReservationService(test_db)

        room = room_service.create_room("Sala D", 3, "Piso 5")

        # Intentar reservar con usuario que no existe
        with pytest.raises(ValueError) as exc_info:
            reservation_service.create_reservation(
                user_id=9999,  # Usuario inexistente
                room_id=room.id,
                reservation_date=date(2025, 6, 1),
                start_hour=14,
                end_hour=16,
            )

        assert "No existe el usuario con ID 9999" in str(exc_info.value)
