"""Module contenant l'énumération des types de tokens."""

from enum import Enum, auto


class TokenType(Enum):
    """Énumération des types de tokens reconnus par l'analyseur lexical.

    Cette énumération définit tous les types de tokens que l'analyseur
    lexical peut produire lors de l'analyse du code source.

    :Example:
        >>> token_type = TokenType.INT
        >>> token_type.name
        'INT'
    """

    # Littéraux
    INT = auto()
    """Token représentant un entier (ex: 42, -10)."""

    FLOAT = auto()
    """Token représentant un nombre flottant (ex: 3.14, -0.5)."""

    STRING = auto()
    """Token représentant une chaîne de caractères (ex: "hello")."""

    # Identifiants
    IDENTIFIANT = auto()
    """Token représentant un identifiant de service (ex: add, calculate)."""

    # Délimiteurs
    LPAREN = auto()
    """Token représentant une parenthèse ouvrante '('."""

    RPAREN = auto()
    """Token représentant une parenthèse fermante ')'."""

    LBRACKET = auto()
    """Token représentant un crochet ouvrant '['."""

    RBRACKET = auto()
    """Token représentant un crochet fermant ']'."""

    COMMA = auto()
    """Token représentant une virgule ','."""

    # Spécial
    EOF = auto()
    """Token représentant la fin du fichier."""

    def __str__(self) -> str:
        """Retourne une représentation en chaîne du type de token.

        :return: Nom du type de token.
        :rtype: str
        """
        return self.name
