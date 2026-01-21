"""Module contenant l'exception pour les erreurs d'analyse syntaxique."""

from baobab_geek_interpreter.exceptions.base_exception import (
    BaobabGeekInterpreterException,
)


class BaobabSyntaxAnalyserException(BaobabGeekInterpreterException):
    """Exception levée lors d'erreurs d'analyse syntaxique.

    Cette exception est levée lorsque l'analyseur syntaxique rencontre
    une erreur pendant la construction de l'arbre syntaxique abstrait (AST).

    :Example:
        >>> raise BaobabSyntaxAnalyserException(
        ...     "Token inattendu: attendu ')', trouvé ','",
        ...     source='service(1, 2',
        ...     position=13,
        ...     line=1,
        ...     column=14
        ... )
    """
