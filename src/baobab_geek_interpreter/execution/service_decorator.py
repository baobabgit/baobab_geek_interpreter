"""Module contenant le décorateur @service pour marquer les services."""

from functools import wraps
from typing import Any, Callable, TypeVar, cast

# TypeVar pour préserver le type de la fonction décorée
F = TypeVar("F", bound=Callable[..., Any])


def service(func: F) -> F:
    """Décorateur pour marquer une fonction comme service.

    Ajoute les métadonnées suivantes à la fonction :
    - `_is_service` : True
    - `_service_name` : nom de la fonction

    :param func: La fonction à décorer.
    :type func: Callable[..., Any]
    :return: La fonction décorée avec les métadonnées.
    :rtype: Callable[..., Any]

    :Example:
        >>> @service
        ... def add(a: int, b: int) -> int:
        ...     return a + b
        >>> hasattr(add, '_is_service')
        True
        >>> add._is_service
        True
        >>> add._service_name
        'add'
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Wrapper qui appelle la fonction originale.

        :param args: Arguments positionnels.
        :param kwargs: Arguments nommés.
        :return: Résultat de la fonction originale.
        """
        return func(*args, **kwargs)

    # Ajouter les métadonnées
    setattr(wrapper, "_is_service", True)
    setattr(wrapper, "_service_name", func.__name__)

    return cast(F, wrapper)
