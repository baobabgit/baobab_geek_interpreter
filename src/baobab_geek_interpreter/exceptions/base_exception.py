"""Module contenant la classe d'exception de base du projet."""

from typing import Optional


class BaobabGeekInterpreterException(Exception):
    """Classe de base pour toutes les exceptions du projet Baobab Geek Interpreter.

    Cette exception sert de classe parente pour toutes les exceptions personnalisées
    du projet. Elle enrichit les exceptions Python standard en ajoutant des informations
    contextuelles utiles pour le débogage.

    :param message: Message d'erreur décrivant l'exception.
    :type message: str
    :param source: Code source complet où l'erreur s'est produite (optionnel).
    :type source: Optional[str]
    :param position: Position du caractère dans la source où l'erreur s'est produite (optionnel).
    :type position: Optional[int]
    :param line: Numéro de ligne où l'erreur s'est produite (optionnel).
    :type line: Optional[int]
    :param column: Numéro de colonne où l'erreur s'est produite (optionnel).
    :type column: Optional[int]

    :ivar message: Message d'erreur.
    :type message: str
    :ivar source: Code source complet.
    :type source: Optional[str]
    :ivar position: Position du caractère dans la source.
    :type position: Optional[int]
    :ivar line: Numéro de ligne.
    :type line: Optional[int]
    :ivar column: Numéro de colonne.
    :type column: Optional[int]

    :Example:
        >>> raise BaobabGeekInterpreterException(
        ...     "Erreur de syntaxe",
        ...     source="service(1, 2)",
        ...     position=7,
        ...     line=1,
        ...     column=8
        ... )
    """

    def __init__(
        self,
        message: str,
        source: Optional[str] = None,
        position: Optional[int] = None,
        line: Optional[int] = None,
        column: Optional[int] = None,
    ) -> None:
        """Initialise une exception Baobab Geek Interpreter.

        :param message: Message d'erreur décrivant l'exception.
        :type message: str
        :param source: Code source complet où l'erreur s'est produite (optionnel).
        :type source: Optional[str]
        :param position: Position du caractère dans la source (optionnel).
        :type position: Optional[int]
        :param line: Numéro de ligne où l'erreur s'est produite (optionnel).
        :type line: Optional[int]
        :param column: Numéro de colonne où l'erreur s'est produite (optionnel).
        :type column: Optional[int]
        """
        super().__init__(message)
        self.message: str = message
        self.source: Optional[str] = source
        self.position: Optional[int] = position
        self.line: Optional[int] = line
        self.column: Optional[int] = column

    def __str__(self) -> str:
        """Retourne une représentation en chaîne formatée de l'exception.

        Si les informations de ligne et de colonne sont disponibles,
        elles sont incluses dans le message.

        :return: Message d'erreur formaté.
        :rtype: str

        :Example:
            >>> exc = BaobabGeekInterpreterException("Test error", line=5, column=10)
            >>> str(exc)
            'Test error at line 5, column 10'
        """
        if self.line is not None and self.column is not None:
            return f"{self.message} at line {self.line}, column {self.column}"
        return self.message
