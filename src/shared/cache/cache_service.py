from datetime import datetime, timedelta
from typing import Any, Optional


class CacheService:
    """
    Servicio de caché en memoria.

    Almacena temporalmente datos para evitar recalcular o consultar la BD.
    En producción, esto podría cambiarse a Redis.

    Uso:
        cache = CacheService()
        cache.set("availability:5:2025-02-19", {"slots": [8,9,10]})
        data = cache.get("availability:5:2025-02-19")
    """

    def __init__(self):
        """Inicializa el caché como un diccionario en memoria."""
        self._cache: dict[str, tuple[Any, datetime]] = {}
        self._default_ttl = 3600  # 1 hora en segundos

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Guarda un valor en el caché.

        Args:
            key: Identificador único (ej: "availability:5:2025-02-19")
            value: Datos a guardar (dict, list, str, etc.)
            ttl: Tiempo de vida en segundos (None = usar default)
        """
        expiration = datetime.now() + timedelta(seconds=ttl or self._default_ttl)
        self._cache[key] = (value, expiration)

    def get(self, key: str) -> Optional[Any]:
        """
        Recupera un valor del caché.

        Args:
            key: Identificador único

        Returns:
            El valor guardado, o None si no existe o expiró
        """
        if key not in self._cache:
            return None

        value, expiration = self._cache[key]

        # Verificar si expiró
        if datetime.now() > expiration:
            del self._cache[key]
            return None

        return value

    def delete(self, key: str) -> bool:
        """
        Elimina una clave del caché.

        Args:
            key: Identificador único

        Returns:
            True si se eliminó, False si no existía
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> None:
        """Limpia todo el caché."""
        self._cache.clear()

    def get_cache_key(self, *parts: str) -> str:
        """
        Construye una clave de caché consistente.

        Args:
            *parts: Componentes de la clave

        Returns:
            Clave formateada (ej: "availability:5:2025-02-19")

        Ejemplo:
            key = cache.get_cache_key("availability", "5", "2025-02-19")
        """
        return ":".join(str(part) for part in parts)


# Singleton: una sola instancia de caché para toda la app
_cache_instance: Optional[CacheService] = None


def get_cache() -> CacheService:
    """
    Retorna la instancia global del servicio de caché.

    Returns:
        Instancia singleton de CacheService
    """
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = CacheService()
    return _cache_instance
