"""Module contenant l'exception pour les erreurs d'analyse lexicale."""

from baobab_geek_interpreter.exceptions.base_exception import (
    BaobabGeekInterpreterException,
)


class BaobabLexicalAnalyserException(BaobabGeekInterpreterException):
    """Exception levée lors d'erreurs d'analyse lexicale.

    Cette exception est levée lorsque l'analyseur lexical rencontre
    une erreur pendant la transformation du code source en tokens.

    :Example:
        >>> raise BaobabLexicalAnalyserException(
        ...     "Chaîne de caractères non fermée",
        ...     source='service("test',
        ...     position=12,
        ...     line=1,
        ...     column=13
        ... )
    """
