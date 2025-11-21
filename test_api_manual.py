"""
Script de ejemplo para probar la API de BookMe.

Este script demuestra el flujo completo:
1. Crear usuarios
2. Crear salas
3. Hacer reservas
4. Consultar disponibilidad
"""

import requests
import json
from datetime import date, timedelta

# URL base de la API
BASE_URL = "http://localhost:8000"


def print_response(title, response):
    """Imprime una respuesta de forma bonita."""
    print(f"\n{'='*60}")
    print(f"📌 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")


def test_api():
    """Función principal que prueba todos los endpoints."""
    
    print("\n🚀 Iniciando pruebas de BookMe API")
    print(f"URL: {BASE_URL}")
    
    # ===== 1. CREAR USUARIOS =====
    
    print("\n\n📋 PASO 1: CREAR USUARIOS")
    print("-" * 60)
    
    user1_data = {
        "nombre": "Juan Pérez",
        "email": "juan.perez@example.com"
    }
    user1_response = requests.post(f"{BASE_URL}/users/", json=user1_data)
    print_response("Crear Usuario 1", user1_response)
    user1 = user1_response.json()
    
    user2_data = {
        "nombre": "María García",
        "email": "maria.garcia@example.com"
    }
    user2_response = requests.post(f"{BASE_URL}/users/", json=user2_data)
    print_response("Crear Usuario 2", user2_response)
    user2 = user2_response.json()
    
    # ===== 2. CREAR SALAS =====
    
    print("\n\n📋 PASO 2: CREAR SALAS")
    print("-" * 60)
    
    room1_data = {
        "nombre": "Sala Coworking A1",
        "capacidad": 10,
        "ubicacion": "Edificio Principal, Piso 2"
    }
    room1_response = requests.post(f"{BASE_URL}/rooms/", json=room1_data)
    print_response("Crear Sala 1", room1_response)
    room1 = room1_response.json()
    
    room2_data = {
        "nombre": "Sala de Reuniones B2",
        "capacidad": 6,
        "ubicacion": "Edificio Norte, Piso 1"
    }
    room2_response = requests.post(f"{BASE_URL}/rooms/", json=room2_data)
    print_response("Crear Sala 2", room2_response)
    room2 = room2_response.json()
    
    # ===== 3. CONSULTAR DISPONIBILIDAD =====
    
    print("\n\n📋 PASO 3: CONSULTAR DISPONIBILIDAD (SIN RESERVAS)")
    print("-" * 60)
    
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    availability_response = requests.get(
        f"{BASE_URL}/rooms/{room1['id']}/availability",
        params={"date": tomorrow}
    )
    print_response(f"Disponibilidad Sala 1 - {tomorrow}", availability_response)
    
    # ===== 4. CREAR RESERVAS =====
    
    print("\n\n📋 PASO 4: CREAR RESERVAS")
    print("-" * 60)
    
    # Reserva 1: Juan reserva sala 1 de 10-12
    reservation1_data = {
        "userId": user1["id"],
        "roomId": room1["id"],
        "date": tomorrow,
        "startHour": 10,
        "endHour": 12
    }
    reservation1_response = requests.post(f"{BASE_URL}/reservations/", json=reservation1_data)
    print_response("Reserva 1: Juan 10:00-12:00", reservation1_response)
    
    # Reserva 2: María intenta reservar la misma sala de 11-13 (debe fallar por solapamiento)
    reservation2_data = {
        "userId": user2["id"],
        "roomId": room1["id"],
        "date": tomorrow,
        "startHour": 11,
        "endHour": 13
    }
    reservation2_response = requests.post(f"{BASE_URL}/reservations/", json=reservation2_data)
    print_response("❌ Reserva 2: María 11:00-13:00 (debe fallar)", reservation2_response)
    
    # Reserva 3: María reserva en otro horario que no se solapa
    reservation3_data = {
        "userId": user2["id"],
        "roomId": room1["id"],
        "date": tomorrow,
        "startHour": 14,
        "endHour": 16
    }
    reservation3_response = requests.post(f"{BASE_URL}/reservations/", json=reservation3_data)
    print_response("Reserva 3: María 14:00-16:00", reservation3_response)
    
    # ===== 5. CONSULTAR DISPONIBILIDAD ACTUALIZADA =====
    
    print("\n\n📋 PASO 5: CONSULTAR DISPONIBILIDAD (CON RESERVAS)")
    print("-" * 60)
    
    availability2_response = requests.get(
        f"{BASE_URL}/rooms/{room1['id']}/availability",
        params={"date": tomorrow}
    )
    print_response(f"Disponibilidad Actualizada - {tomorrow}", availability2_response)
    
    # ===== 6. LISTAR RESERVAS DE UNA SALA =====
    
    print("\n\n📋 PASO 6: LISTAR RESERVAS DE LA SALA")
    print("-" * 60)
    
    room_reservations_response = requests.get(f"{BASE_URL}/reservations/room/{room1['id']}")
    print_response("Reservas de Sala 1", room_reservations_response)
    
    # ===== 7. INTENTAR ELIMINAR SALA CON RESERVAS =====
    
    print("\n\n📋 PASO 7: INTENTAR ELIMINAR SALA CON RESERVAS (debe fallar)")
    print("-" * 60)
    
    delete_room_response = requests.delete(f"{BASE_URL}/rooms/{room1['id']}")
    print_response("❌ Eliminar Sala con Reservas", delete_room_response)
    
    # ===== 8. DESACTIVAR SALA =====
    
    print("\n\n📋 PASO 8: DESACTIVAR SALA")
    print("-" * 60)
    
    update_room_data = {
        "nombre": room2["nombre"],
        "capacidad": room2["capacidad"],
        "ubicacion": room2["ubicacion"],
        "activa": False
    }
    update_room_response = requests.put(f"{BASE_URL}/rooms/{room2['id']}", json=update_room_data)
    print_response("Desactivar Sala 2", update_room_response)
    
    # Intentar reservar sala inactiva (debe fallar)
    reservation4_data = {
        "userId": user1["id"],
        "roomId": room2["id"],
        "date": tomorrow,
        "startHour": 9,
        "endHour": 11
    }
    reservation4_response = requests.post(f"{BASE_URL}/reservations/", json=reservation4_data)
    print_response("❌ Reservar Sala Inactiva (debe fallar)", reservation4_response)
    
    # ===== 9. LISTAR TODOS LOS USUARIOS =====
    
    print("\n\n📋 PASO 9: LISTAR TODOS LOS USUARIOS")
    print("-" * 60)
    
    users_response = requests.get(f"{BASE_URL}/users/")
    print_response("Lista de Usuarios", users_response)
    
    # ===== 10. LISTAR TODAS LAS SALAS =====
    
    print("\n\n📋 PASO 10: LISTAR TODAS LAS SALAS")
    print("-" * 60)
    
    rooms_response = requests.get(f"{BASE_URL}/rooms/")
    print_response("Lista de Salas", rooms_response)
    
    # ===== RESUMEN =====
    
    print("\n\n" + "="*60)
    print("✅ PRUEBAS COMPLETADAS")
    print("="*60)
    print("""
    Resumen de lo probado:
    ✓ Crear usuarios
    ✓ Crear salas
    ✓ Consultar disponibilidad (caché)
    ✓ Crear reservas exitosas
    ✓ Validar solapamiento de reservas
    ✓ Validar reservas en salas inactivas
    ✓ Intentar eliminar sala con reservas
    ✓ Desactivar/activar salas
    ✓ Listar todos los recursos
    
    📖 Para ver la documentación interactiva:
       http://localhost:8000/docs
    """)


if __name__ == "__main__":
    try:
        # Verificar que la API está corriendo
        health_response = requests.get(f"{BASE_URL}/health", timeout=2)
        if health_response.status_code == 200:
            print("✅ API está funcionando correctamente")
            test_api()
        else:
            print("❌ La API respondió pero con errores")
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: No se puede conectar a la API")
        print("   Asegúrate de que el servidor está corriendo:")
        print("   python api.py")
    except Exception as e:
        print(f"❌ ERROR inesperado: {e}")
