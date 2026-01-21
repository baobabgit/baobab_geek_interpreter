"""Module pour l'exécution de l'AST."""

from typing import Any

from baobab_geek_interpreter.exceptions.execution_exception import (
    BaobabExecutionException,
)
from baobab_geek_interpreter.semantic.symbol_table import SymbolTable
from baobab_geek_interpreter.syntax.ast_node import (
    ASTVisitor,
    ArrayNode,
    FloatNode,
    IntNode,
    ServiceCallNode,
    StringNode,
)


class Executor(ASTVisitor):
    """Exécuteur pour interpréter l'AST et appeler les services.

    Implémente le pattern Visitor pour parcourir l'AST et exécuter
    les services enregistrés dans la table des symboles.

    :param symbol_table: Table des symboles contenant les services enregistrés.
    :type symbol_table: SymbolTable

    :Example:
        >>> from baobab_geek_interpreter.semantic.symbol_table import SymbolTable
        >>> table = SymbolTable()
        >>> def add(a: int, b: int) -> int:
        ...     return a + b
        >>> table.register("add", add)
        >>> executor = Executor(table)
    """

    def __init__(self, symbol_table: SymbolTable) -> None:
        """Initialise l'exécuteur.

        :param symbol_table: Table des symboles.
        :type symbol_table: SymbolTable
        """
        self._symbol_table = symbol_table

    def execute(self, ast: ServiceCallNode) -> Any:
        """Exécute un AST et retourne le résultat.

        :param ast: Nœud racine de l'AST à exécuter.
        :type ast: ServiceCallNode
        :return: Résultat de l'exécution du service.
        :rtype: Any
        :raises BaobabExecutionException: Si une erreur survient pendant l'exécution.

        :Example:
            >>> # ast = ServiceCallNode("add", [IntNode(1), IntNode(2)])
            >>> # result = executor.execute(ast)
            >>> # result == 3
        """
        return ast.accept(self)

    def visit_service_call(self, node: ServiceCallNode) -> Any:
        """Visite un nœud d'appel de service et exécute le service.

        :param node: Nœud d'appel de service.
        :type node: ServiceCallNode
        :return: Résultat de l'exécution du service.
        :rtype: Any
        :raises BaobabExecutionException: Si le service lève une exception.
        """
        service_name = node.name
        service_func = self._symbol_table.get(service_name)

        if service_func is None:
            raise BaobabExecutionException(
                f"Service '{service_name}' non trouvé",
                source="",
                position=0,
                line=0,
                column=0,
                service_name=service_name,
                original_exception=None,
            )

        # Évaluer les arguments
        args = [arg.accept(self) for arg in node.arguments]

        # Exécuter le service
        try:
            return service_func(*args)
        except Exception as exc:
            raise BaobabExecutionException(
                f"Erreur lors de l'exécution du service '{service_name}': {str(exc)}",
                source="",
                position=0,
                line=0,
                column=0,
                service_name=service_name,
                original_exception=exc,
            ) from exc

    def visit_argument(self, node: Any) -> Any:
        """Visite un nœud d'argument et retourne sa valeur.

        :param node: Nœud d'argument.
        :type node: Any
        :return: Valeur de l'argument.
        :rtype: Any
        """
        # Les arguments contiennent un nœud de valeur
        return node.value.accept(self)

    def visit_int(self, node: IntNode) -> int:
        """Visite un nœud d'entier et retourne sa valeur.

        :param node: Nœud d'entier.
        :type node: IntNode
        :return: Valeur entière.
        :rtype: int
        """
        return node.value

    def visit_float(self, node: FloatNode) -> float:
        """Visite un nœud de flottant et retourne sa valeur.

        :param node: Nœud de flottant.
        :type node: FloatNode
        :return: Valeur flottante.
        :rtype: float
        """
        return node.value

    def visit_string(self, node: StringNode) -> str:
        """Visite un nœud de chaîne et retourne sa valeur.

        :param node: Nœud de chaîne.
        :type node: StringNode
        :return: Valeur de la chaîne.
        :rtype: str
        """
        return node.value

    def visit_array(self, node: ArrayNode) -> list[Any]:
        """Visite un nœud de tableau et retourne une liste Python.

        :param node: Nœud de tableau.
        :type node: ArrayNode
        :return: Liste Python contenant les valeurs du tableau.
        :rtype: list[Any]
        """
        return [elem.accept(self) for elem in node.elements]
