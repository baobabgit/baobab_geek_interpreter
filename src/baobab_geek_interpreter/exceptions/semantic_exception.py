"""Module contenant l'exception pour les erreurs d'analyse sémantique."""

from baobab_geek_interpreter.exceptions.base_exception import (
    BaobabGeekInterpreterException,
)


class BaobabSemanticAnalyserException(BaobabGeekInterpreterException):
    """Exception levée lors d'erreurs d'analyse sémantique.

    Cette exception est levée lorsque l'analyseur sémantique détecte
    une erreur de validation (service inexistant, types incompatibles, etc.).

    :Example:
        >>> raise BaobabSemanticAnalyserException(
        ...     "Service 'unknown_service' non trouvé",
        ...     source='unknown_service()',
        ...     position=0,
        ...     line=1,
        ...     column=1
        ... )
    """
