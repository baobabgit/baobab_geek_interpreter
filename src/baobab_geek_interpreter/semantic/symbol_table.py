"""Module contenant la table des symboles pour gérer les services enregistrés."""

import inspect
from typing import Any, Callable, Dict, List, Optional


class SymbolTable:
    """Table des symboles pour gérer les services enregistrés.

    Permet d'enregistrer, rechercher et lister les services disponibles.
    Supporte également la découverte automatique des services dans un module.

    :ivar _symbols: Dictionnaire associant les noms de services aux fonctions.
    :type _symbols: Dict[str, Callable[..., Any]]

    :Example:
        >>> table = SymbolTable()
        >>> def my_service():
        ...     return "result"
        >>> table.register("my_service", my_service)
        >>> table.has("my_service")
        True
    """

    def __init__(self) -> None:
        """Initialise une table des symboles vide."""
        self._symbols: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, func: Callable[..., Any]) -> None:
        """Enregistre un service dans la table des symboles.

        Si un service avec le même nom existe déjà, il est écrasé.

        :param name: Nom du service à enregistrer.
        :type name: str
        :param func: Fonction callable du service.
        :type func: Callable[..., Any]

        :Example:
            >>> table = SymbolTable()
            >>> def add(a, b):
            ...     return a + b
            >>> table.register("add", add)
            >>> table.has("add")
            True
        """
        self._symbols[name] = func

    def get(self, name: str) -> Optional[Callable[..., Any]]:
        """Récupère un service par son nom.

        :param name: Nom du service à récupérer.
        :type name: str
        :return: La fonction du service, ou None si non trouvé.
        :rtype: Optional[Callable[..., Any]]

        :Example:
            >>> table = SymbolTable()
            >>> def multiply(a, b):
            ...     return a * b
            >>> table.register("multiply", multiply)
            >>> func = table.get("multiply")
            >>> func(3, 4)
            12
        """
        return self._symbols.get(name)

    def has(self, name: str) -> bool:
        """Vérifie si un service existe dans la table.

        :param name: Nom du service à vérifier.
        :type name: str
        :return: True si le service existe, False sinon.
        :rtype: bool

        :Example:
            >>> table = SymbolTable()
            >>> table.has("unknown")
            False
            >>> def test():
            ...     pass
            >>> table.register("test", test)
            >>> table.has("test")
            True
        """
        return name in self._symbols

    def discover_services(self, module: Any) -> None:
        """Découvre et enregistre automatiquement les services dans un module.

        Parcourt tous les membres du module et enregistre ceux qui ont
        l'attribut `_is_service` à True.

        :param module: Module Python à analyser.
        :type module: Any

        :Example:
            >>> # Dans un module example.py:
            >>> # @service
            >>> # def my_func():
            >>> #     pass
            >>> import example
            >>> table = SymbolTable()
            >>> table.discover_services(example)
            >>> table.has("my_func")
            True
        """
        for name, obj in inspect.getmembers(module):
            # Vérifier si c'est un service
            # pylint: disable=protected-access
            if callable(obj) and hasattr(obj, "_is_service") and obj._is_service:
                service_name = getattr(obj, "_service_name", name)
                self.register(service_name, obj)

    def list_services(self) -> List[str]:
        """Liste tous les noms de services enregistrés.

        :return: Liste des noms de services.
        :rtype: List[str]

        :Example:
            >>> table = SymbolTable()
            >>> table.register("service1", lambda: None)
            >>> table.register("service2", lambda: None)
            >>> sorted(table.list_services())
            ['service1', 'service2']
        """
        return list(self._symbols.keys())

    def clear(self) -> None:
        """Vide la table des symboles.

        Supprime tous les services enregistrés.

        :Example:
            >>> table = SymbolTable()
            >>> table.register("test", lambda: None)
            >>> len(table.list_services())
            1
            >>> table.clear()
            >>> len(table.list_services())
            0
        """
        self._symbols.clear()
