"""Module contenant les classes de l'arbre syntaxique abstrait (AST)."""

from abc import ABC, abstractmethod
from typing import Any, List


class ASTVisitor(ABC):
    """Interface abstraite pour le pattern Visitor sur l'AST.

    Le pattern Visitor permet de parcourir et traiter les nœuds
    de l'arbre syntaxique sans modifier leurs classes.

    :Example:
        >>> class MyVisitor(ASTVisitor):
        ...     def visit_int(self, node):
        ...         return node.value * 2
    """

    @abstractmethod
    def visit_service_call(self, node: "ServiceCallNode") -> Any:
        """Visite un nœud d'appel de service.

        :param node: Nœud à visiter.
        :type node: ServiceCallNode
        :return: Résultat de la visite.
        :rtype: Any
        """

    @abstractmethod
    def visit_argument(self, node: "ArgumentNode") -> Any:
        """Visite un nœud d'argument.

        :param node: Nœud à visiter.
        :type node: ArgumentNode
        :return: Résultat de la visite.
        :rtype: Any
        """

    @abstractmethod
    def visit_int(self, node: "IntNode") -> Any:
        """Visite un nœud d'entier.

        :param node: Nœud à visiter.
        :type node: IntNode
        :return: Résultat de la visite.
        :rtype: Any
        """

    @abstractmethod
    def visit_float(self, node: "FloatNode") -> Any:
        """Visite un nœud de flottant.

        :param node: Nœud à visiter.
        :type node: FloatNode
        :return: Résultat de la visite.
        :rtype: Any
        """

    @abstractmethod
    def visit_string(self, node: "StringNode") -> Any:
        """Visite un nœud de chaîne de caractères.

        :param node: Nœud à visiter.
        :type node: StringNode
        :return: Résultat de la visite.
        :rtype: Any
        """

    @abstractmethod
    def visit_array(self, node: "ArrayNode") -> Any:
        """Visite un nœud de tableau.

        :param node: Nœud à visiter.
        :type node: ArrayNode
        :return: Résultat de la visite.
        :rtype: Any
        """


class ASTNode(ABC):
    """Classe de base abstraite pour tous les nœuds de l'AST.

    Chaque nœud représente une construction syntaxique du langage
    et implémente la méthode accept() pour le pattern Visitor.
    """

    @abstractmethod
    def accept(self, visitor: ASTVisitor) -> Any:
        """Accepte un visiteur (pattern Visitor).

        :param visitor: Visiteur à accepter.
        :type visitor: ASTVisitor
        :return: Résultat de la visite.
        :rtype: Any
        """


class ServiceCallNode(ASTNode):
    """Nœud représentant un appel de service.

    :param name: Nom du service à appeler.
    :type name: str
    :param arguments: Liste des arguments de l'appel.
    :type arguments: List[ArgumentNode]

    :ivar name: Nom du service.
    :type name: str
    :ivar arguments: Liste des arguments.
    :type arguments: List[ArgumentNode]

    :Example:
        >>> node = ServiceCallNode("add", [arg1, arg2])
        >>> node.name
        'add'
    """

    def __init__(self, name: str, arguments: List["ArgumentNode"]) -> None:
        """Initialise un nœud d'appel de service.

        :param name: Nom du service.
        :type name: str
        :param arguments: Liste des arguments.
        :type arguments: List[ArgumentNode]
        """
        self.name: str = name
        self.arguments: List[ArgumentNode] = arguments

    def accept(self, visitor: ASTVisitor) -> Any:
        """Accepte un visiteur.

        :param visitor: Visiteur à accepter.
        :type visitor: ASTVisitor
        :return: Résultat de la visite.
        :rtype: Any
        """
        return visitor.visit_service_call(self)


class ArgumentNode(ASTNode):
    """Nœud représentant un argument d'appel de service.

    :param value: Valeur constante de l'argument.
    :type value: ConstantNode

    :ivar value: Valeur de l'argument.
    :type value: ConstantNode

    :Example:
        >>> int_node = IntNode(42)
        >>> arg = ArgumentNode(int_node)
    """

    def __init__(self, value: "ConstantNode") -> None:
        """Initialise un nœud d'argument.

        :param value: Valeur constante de l'argument.
        :type value: ConstantNode
        """
        self.value: ConstantNode = value

    def accept(self, visitor: ASTVisitor) -> Any:
        """Accepte un visiteur.

        :param visitor: Visiteur à accepter.
        :type visitor: ASTVisitor
        :return: Résultat de la visite.
        :rtype: Any
        """
        return visitor.visit_argument(self)


class ConstantNode(ASTNode):
    """Classe de base abstraite pour les nœuds de constantes.

    Les constantes sont des valeurs littérales comme les entiers,
    flottants, chaînes, ou tableaux.
    """


class IntNode(ConstantNode):
    """Nœud représentant un entier.

    :param value: Valeur entière.
    :type value: int

    :ivar value: Valeur entière.
    :type value: int

    :Example:
        >>> node = IntNode(42)
        >>> node.value
        42
    """

    def __init__(self, value: int) -> None:
        """Initialise un nœud d'entier.

        :param value: Valeur entière.
        :type value: int
        """
        self.value: int = value

    def accept(self, visitor: ASTVisitor) -> Any:
        """Accepte un visiteur.

        :param visitor: Visiteur à accepter.
        :type visitor: ASTVisitor
        :return: Résultat de la visite.
        :rtype: Any
        """
        return visitor.visit_int(self)


class FloatNode(ConstantNode):
    """Nœud représentant un flottant.

    :param value: Valeur flottante.
    :type value: float

    :ivar value: Valeur flottante.
    :type value: float

    :Example:
        >>> node = FloatNode(3.14)
        >>> node.value
        3.14
    """

    def __init__(self, value: float) -> None:
        """Initialise un nœud de flottant.

        :param value: Valeur flottante.
        :type value: float
        """
        self.value: float = value

    def accept(self, visitor: ASTVisitor) -> Any:
        """Accepte un visiteur.

        :param visitor: Visiteur à accepter.
        :type visitor: ASTVisitor
        :return: Résultat de la visite.
        :rtype: Any
        """
        return visitor.visit_float(self)


class StringNode(ConstantNode):
    """Nœud représentant une chaîne de caractères.

    :param value: Valeur de la chaîne.
    :type value: str

    :ivar value: Valeur de la chaîne.
    :type value: str

    :Example:
        >>> node = StringNode("hello")
        >>> node.value
        'hello'
    """

    def __init__(self, value: str) -> None:
        """Initialise un nœud de chaîne.

        :param value: Valeur de la chaîne.
        :type value: str
        """
        self.value: str = value

    def accept(self, visitor: ASTVisitor) -> Any:
        """Accepte un visiteur.

        :param visitor: Visiteur à accepter.
        :type visitor: ASTVisitor
        :return: Résultat de la visite.
        :rtype: Any
        """
        return visitor.visit_string(self)


class ArrayNode(ConstantNode):
    """Nœud représentant un tableau de constantes.

    :param elements: Liste des éléments du tableau.
    :type elements: List[ConstantNode]

    :ivar elements: Liste des éléments.
    :type elements: List[ConstantNode]

    :Example:
        >>> node = ArrayNode([IntNode(1), IntNode(2)])
        >>> len(node.elements)
        2
    """

    def __init__(self, elements: List[ConstantNode]) -> None:
        """Initialise un nœud de tableau.

        :param elements: Liste des éléments du tableau.
        :type elements: List[ConstantNode]
        """
        self.elements: List[ConstantNode] = elements

    def accept(self, visitor: ASTVisitor) -> Any:
        """Accepte un visiteur.

        :param visitor: Visiteur à accepter.
        :type visitor: ASTVisitor
        :return: Résultat de la visite.
        :rtype: Any
        """
        return visitor.visit_array(self)
