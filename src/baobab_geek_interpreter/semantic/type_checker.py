"""Module pour la vérification des types."""

import inspect
from typing import Any, Callable, List, get_args, get_origin


class TypeChecker:
    """Vérificateur de types pour la validation des arguments de service.

    Effectue une validation stricte des types sans conversion automatique.
    Support des types: int, float, str, list[T].

    :Example:
        >>> checker = TypeChecker()
        >>> def my_func(a: int, b: str) -> None:
        ...     pass
        >>> checker.check_types(my_func, [42, "hello"])
        True
    """

    @staticmethod
    def check_types(func: Callable[..., Any], args: List[Any]) -> bool:
        """Vérifie que les types des arguments correspondent à la signature.

        Validation stricte sans conversion automatique.

        :param func: Fonction dont on vérifie la signature.
        :type func: Callable[..., Any]
        :param args: Arguments à valider.
        :type args: List[Any]
        :return: True si les types correspondent, False sinon.
        :rtype: bool

        :Example:
            >>> def add(a: int, b: int) -> int:
            ...     return a + b
            >>> TypeChecker.check_types(add, [1, 2])
            True
            >>> TypeChecker.check_types(add, [1, "2"])
            False
        """
        signature = inspect.signature(func)
        params = list(signature.parameters.values())

        # Vérifier le nombre d'arguments
        if len(args) != len(params):
            return False

        # Vérifier chaque argument
        for arg, param in zip(args, params):
            if param.annotation == inspect.Parameter.empty:
                # Pas de type annoté, on accepte tout
                continue

            expected_type = param.annotation
            if not TypeChecker._check_single_type(arg, expected_type):
                return False

        return True

    @staticmethod
    def _check_single_type(value: Any, expected_type: Any) -> bool:
        """Vérifie qu'une valeur correspond à un type attendu.

        :param value: Valeur à vérifier.
        :type value: Any
        :param expected_type: Type attendu.
        :type expected_type: Any
        :return: True si le type correspond.
        :rtype: bool
        """
        # Gérer les types génériques (list[int], etc.)
        origin = get_origin(expected_type)
        if origin is list:
            # C'est un type list[T]
            if not isinstance(value, list):
                return False
            # Vérifier l'homogénéité du tableau
            type_args = get_args(expected_type)
            if type_args:
                element_type = type_args[0]
                return all(TypeChecker._check_single_type(item, element_type) for item in value)
            return True

        # Type simple
        return isinstance(value, expected_type)

    @staticmethod
    def is_array_homogeneous(array: List[Any]) -> bool:
        """Vérifie qu'un tableau est homogène (tous les éléments du même type).

        :param array: Tableau à vérifier.
        :type array: List[Any]
        :return: True si homogène.
        :rtype: bool

        :Example:
            >>> TypeChecker.is_array_homogeneous([1, 2, 3])
            True
            >>> TypeChecker.is_array_homogeneous([1, "2", 3])
            False
        """
        if not array:
            return True  # Un tableau vide est homogène

        first_type = type(array[0])
        return all(isinstance(item, first_type) for item in array)

    @staticmethod
    def has_nested_arrays(array: List[Any]) -> bool:
        """Vérifie si un tableau contient des tableaux imbriqués.

        :param array: Tableau à vérifier.
        :type array: List[Any]
        :return: True si des tableaux sont imbriqués.
        :rtype: bool

        :Example:
            >>> TypeChecker.has_nested_arrays([1, 2, 3])
            False
            >>> TypeChecker.has_nested_arrays([[1, 2], [3, 4]])
            True
        """
        return any(isinstance(item, list) for item in array)

    @staticmethod
    def get_array_element_type(array: List[Any]) -> type:
        """Retourne le type des éléments d'un tableau homogène.

        :param array: Tableau homogène.
        :type array: List[Any]
        :return: Type des éléments.
        :rtype: type
        :raises ValueError: Si le tableau est vide ou hétérogène.

        :Example:
            >>> TypeChecker.get_array_element_type([1, 2, 3])
            <class 'int'>
        """
        if not array:
            raise ValueError("Cannot determine type of empty array")
        if not TypeChecker.is_array_homogeneous(array):
            raise ValueError("Array is not homogeneous")
        return type(array[0])
