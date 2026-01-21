"""Module pour l'analyse sémantique de l'AST."""

from typing import Any, List

from baobab_geek_interpreter.exceptions.semantic_exception import (
    BaobabSemanticAnalyserException,
)
from baobab_geek_interpreter.semantic.symbol_table import SymbolTable
from baobab_geek_interpreter.semantic.type_checker import TypeChecker
from baobab_geek_interpreter.syntax.ast_node import (
    ArrayNode,
    ServiceCallNode,
)


class SemanticAnalyzer:
    """Analyseur sémantique pour valider l'AST avant l'exécution.

    Effectue les vérifications suivantes :
    - Service existe dans la table des symboles
    - Nombre d'arguments correct
    - Types d'arguments compatibles
    - Tableaux homogènes
    - Pas de tableaux imbriqués (v1.0)

    :param symbol_table: Table des symboles contenant les services enregistrés.
    :type symbol_table: SymbolTable

    :Example:
        >>> from baobab_geek_interpreter.semantic.symbol_table import SymbolTable
        >>> table = SymbolTable()
        >>> def add(a: int, b: int) -> int:
        ...     return a + b
        >>> table.register("add", add)
        >>> analyzer = SemanticAnalyzer(table)
    """

    def __init__(self, symbol_table: SymbolTable) -> None:
        """Initialise l'analyseur sémantique.

        :param symbol_table: Table des symboles.
        :type symbol_table: SymbolTable
        """
        self._symbol_table = symbol_table
        self._type_checker = TypeChecker()

    def analyze(self, ast: ServiceCallNode) -> None:
        """Analyse un AST et valide les règles sémantiques.

        :param ast: Nœud racine de l'AST à analyser.
        :type ast: ServiceCallNode
        :raises BaobabSemanticAnalyserException: Si une erreur sémantique est détectée.

        :Example:
            >>> # ast = ServiceCallNode("add", [IntNode(1), IntNode(2)])
            >>> # analyzer.analyze(ast)
        """
        # Vérifier que le service existe
        service_name = ast.name
        service_func = self._symbol_table.get(service_name)

        if service_func is None:
            raise BaobabSemanticAnalyserException(
                f"Service inconnu : '{service_name}'",
                source="",
                position=0,
                line=0,
                column=0,
            )

        # Extraire les valeurs des arguments
        arg_values = self._extract_argument_values(ast)

        # Vérifier les tableaux (homogénéité et imbrication)
        self._check_arrays(arg_values)

        # Vérifier les types avec la signature du service
        if not self._type_checker.check_types(service_func, arg_values):
            raise BaobabSemanticAnalyserException(
                f"Types d'arguments incompatibles pour le service '{service_name}'",
                source="",
                position=0,
                line=0,
                column=0,
            )

    def _extract_argument_values(self, ast: ServiceCallNode) -> List[Any]:
        """Extrait les valeurs concrètes des arguments.

        :param ast: Nœud d'appel de service.
        :type ast: ServiceCallNode
        :return: Liste des valeurs des arguments.
        :rtype: List[Any]
        """
        values = []
        for arg_node in ast.arguments:
            value_node = arg_node.value
            if isinstance(value_node, ArrayNode):
                # Extraire les valeurs du tableau
                array_values = []
                for elem in value_node.elements:
                    if isinstance(elem, ArrayNode):
                        # Tableau imbriqué - extraire récursivement
                        nested_values = [
                            nested_elem.value  # type: ignore[attr-defined]
                            for nested_elem in elem.elements
                        ]
                        array_values.append(nested_values)
                    else:
                        # Valeur simple
                        array_values.append(elem.value)  # type: ignore[attr-defined]
                values.append(array_values)
            else:
                # Valeur simple (int, float, string)
                values.append(value_node.value)  # type: ignore[attr-defined]
        return values

    def _check_arrays(self, arg_values: List[Any]) -> None:
        """Vérifie que tous les tableaux sont homogènes et non imbriqués.

        :param arg_values: Valeurs des arguments à vérifier.
        :type arg_values: List[Any]
        :raises BaobabSemanticAnalyserException: Si un tableau est invalide.
        """
        for value in arg_values:
            if isinstance(value, list):
                # Vérifier l'homogénéité
                if not self._type_checker.is_array_homogeneous(value):
                    raise BaobabSemanticAnalyserException(
                        "Les tableaux doivent être homogènes (tous les éléments du même type)",
                        source="",
                        position=0,
                        line=0,
                        column=0,
                    )

                # Vérifier l'absence de tableaux imbriqués
                if self._type_checker.has_nested_arrays(value):
                    raise BaobabSemanticAnalyserException(
                        "Les tableaux imbriqués ne sont pas supportés dans cette version",
                        source="",
                        position=0,
                        line=0,
                        column=0,
                    )
