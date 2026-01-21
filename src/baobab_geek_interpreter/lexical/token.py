"""Module contenant la classe Token."""

from typing import Any

from baobab_geek_interpreter.lexical.token_type import TokenType


class Token:
    """Représente une unité lexicale (token) produite par l'analyseur lexical.

    Un token est une unité de base du langage, comme un nombre, un identifiant,
    ou un délimiteur. Chaque token contient son type, sa valeur, et des informations
    de position dans le code source.

    :param token_type: Type du token.
    :type token_type: TokenType
    :param value: Valeur associée au token.
    :type value: Any
    :param position: Position du premier caractère du token dans la source.
    :type position: int
    :param line: Numéro de ligne où se trouve le token (commence à 1).
    :type line: int
    :param column: Numéro de colonne où se trouve le token (commence à 1).
    :type column: int

    :ivar type: Type du token.
    :type type: TokenType
    :ivar value: Valeur associée au token.
    :type value: Any
    :ivar position: Position du premier caractère du token.
    :type position: int
    :ivar line: Numéro de ligne.
    :type line: int
    :ivar column: Numéro de colonne.
    :type column: int

    :Example:
        >>> token = Token(TokenType.INT, 42, 0, 1, 1)
        >>> token.type
        <TokenType.INT: 1>
        >>> token.value
        42
    """

    def __init__(
        self,
        token_type: TokenType,
        value: Any,
        position: int,
        line: int,
        column: int,
    ) -> None:
        """Initialise un token.

        :param token_type: Type du token.
        :type token_type: TokenType
        :param value: Valeur associée au token.
        :type value: Any
        :param position: Position du premier caractère du token.
        :type position: int
        :param line: Numéro de ligne où se trouve le token.
        :type line: int
        :param column: Numéro de colonne où se trouve le token.
        :type column: int
        """
        self.type: TokenType = token_type
        self.value: Any = value
        self.position: int = position
        self.line: int = line
        self.column: int = column

    def __repr__(self) -> str:
        """Retourne une représentation technique du token.

        :return: Représentation du token sous forme de chaîne.
        :rtype: str

        :Example:
            >>> token = Token(TokenType.INT, 42, 0, 1, 1)
            >>> repr(token)
            "Token(INT, 42, pos=0, line=1, col=1)"
        """
        return (
            f"Token({self.type.name}, {self.value!r}, "
            f"pos={self.position}, line={self.line}, col={self.column})"
        )

    def __str__(self) -> str:
        """Retourne une représentation lisible du token.

        :return: Représentation lisible du token.
        :rtype: str

        :Example:
            >>> token = Token(TokenType.INT, 42, 0, 1, 1)
            >>> str(token)
            'INT(42)'
        """
        return f"{self.type.name}({self.value!r})"

    def __eq__(self, other: object) -> bool:
        """Compare deux tokens pour l'égalité.

        Deux tokens sont égaux s'ils ont le même type, la même valeur,
        et la même position.

        :param other: Autre objet à comparer.
        :type other: object
        :return: True si les tokens sont égaux, False sinon.
        :rtype: bool

        :Example:
            >>> token1 = Token(TokenType.INT, 42, 0, 1, 1)
            >>> token2 = Token(TokenType.INT, 42, 0, 1, 1)
            >>> token1 == token2
            True
        """
        if not isinstance(other, Token):
            return False
        return (
            self.type == other.type
            and self.value == other.value
            and self.position == other.position
            and self.line == other.line
            and self.column == other.column
        )
