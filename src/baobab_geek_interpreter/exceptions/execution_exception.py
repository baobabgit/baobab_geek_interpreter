"""Module contenant l'exception pour les erreurs d'exécution."""

from typing import Optional

from baobab_geek_interpreter.exceptions.base_exception import (
    BaobabGeekInterpreterException,
)


class BaobabExecutionException(BaobabGeekInterpreterException):
    """Exception levée lors d'erreurs d'exécution d'un service.

    Cette exception encapsule les exceptions levées par les services
    Python pendant leur exécution, en ajoutant le contexte du service appelé.

    :param message: Message d'erreur décrivant l'exception.
    :type message: str
    :param service_name: Nom du service qui a levé l'exception.
    :type service_name: str
    :param original_exception: Exception d'origine levée par le service (optionnel).
    :type original_exception: Optional[Exception]
    :param source: Code source complet où l'erreur s'est produite (optionnel).
    :type source: Optional[str]
    :param position: Position du caractère dans la source (optionnel).
    :type position: Optional[int]
    :param line: Numéro de ligne où l'erreur s'est produite (optionnel).
    :type line: Optional[int]
    :param column: Numéro de colonne où l'erreur s'est produite (optionnel).
    :type column: Optional[int]

    :ivar service_name: Nom du service.
    :type service_name: str
    :ivar original_exception: Exception d'origine.
    :type original_exception: Optional[Exception]

    :Example:
        >>> try:
        ...     result = 10 / 0
        ... except ZeroDivisionError as e:
        ...     raise BaobabExecutionException(
        ...         "Erreur lors de l'exécution du service 'divide'",
        ...         service_name="divide",
        ...         original_exception=e,
        ...         source="divide(10, 0)",
        ...         line=1,
        ...         column=1
        ...     )
    """

    def __init__(
        self,
        message: str,
        service_name: str,
        original_exception: Optional[Exception] = None,
        source: Optional[str] = None,
        position: Optional[int] = None,
        line: Optional[int] = None,
        column: Optional[int] = None,
    ) -> None:
        """Initialise une exception d'exécution.

        :param message: Message d'erreur décrivant l'exception.
        :type message: str
        :param service_name: Nom du service qui a levé l'exception.
        :type service_name: str
        :param original_exception: Exception d'origine (optionnel).
        :type original_exception: Optional[Exception]
        :param source: Code source complet (optionnel).
        :type source: Optional[str]
        :param position: Position du caractère dans la source (optionnel).
        :type position: Optional[int]
        :param line: Numéro de ligne (optionnel).
        :type line: Optional[int]
        :param column: Numéro de colonne (optionnel).
        :type column: Optional[int]
        """
        super().__init__(
            message=message,
            source=source,
            position=position,
            line=line,
            column=column,
        )
        self.service_name: str = service_name
        self.original_exception: Optional[Exception] = original_exception

    def __str__(self) -> str:
        """Retourne une représentation en chaîne formatée de l'exception.

        Inclut le nom du service et l'exception d'origine si disponible.

        :return: Message d'erreur formaté.
        :rtype: str

        :Example:
            >>> exc = BaobabExecutionException(
            ...     "Division by zero", service_name="divide",
            ...     original_exception=ZeroDivisionError("division by zero")
            ... )
            >>> str(exc)
            "Division by zero in service 'divide': division by zero"
        """
        base_message = self.message
        if self.line is not None and self.column is not None:
            base_message = f"{base_message} at line {self.line}, column {self.column}"

        service_info = f" in service '{self.service_name}'"

        if self.original_exception:
            return f"{base_message}{service_info}: {str(self.original_exception)}"

        return f"{base_message}{service_info}"
