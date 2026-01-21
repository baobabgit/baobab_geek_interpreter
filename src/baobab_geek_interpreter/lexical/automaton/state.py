"""Module contenant la classe State pour les automates finis déterministes."""


class State:
    """Représente un état dans un automate fini déterministe.

    Un état est une unité de base d'un automate. Il peut être soit un état
    normal, soit un état final (acceptant). Les états sont identifiés de manière
    unique par leur nom.

    :param name: Nom unique de l'état.
    :type name: str
    :param is_final: Indique si l'état est acceptant (final).
    :type is_final: bool

    :ivar name: Nom unique de l'état.
    :type name: str
    :ivar is_final: Indique si l'état est acceptant.
    :type is_final: bool

    :Example:
        >>> start = State("START", is_final=False)
        >>> end = State("END", is_final=True)
        >>> start.name
        'START'
        >>> end.is_final
        True
    """

    def __init__(self, name: str, is_final: bool = False) -> None:
        """Initialise un état.

        :param name: Nom unique de l'état.
        :type name: str
        :param is_final: Indique si l'état est acceptant (défaut: False).
        :type is_final: bool
        """
        self.name: str = name
        self.is_final: bool = is_final

    def __eq__(self, other: object) -> bool:
        """Compare deux états pour l'égalité.

        Deux états sont considérés égaux s'ils ont le même nom.

        :param other: Autre objet à comparer.
        :type other: object
        :return: True si les états ont le même nom, False sinon.
        :rtype: bool

        :Example:
            >>> state1 = State("START")
            >>> state2 = State("START")
            >>> state1 == state2
            True
        """
        if not isinstance(other, State):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        """Retourne le hash de l'état.

        Le hash est basé sur le nom de l'état, permettant son utilisation
        dans des sets et comme clé de dictionnaire.

        :return: Hash de l'état.
        :rtype: int

        :Example:
            >>> state1 = State("START")
            >>> state2 = State("START")
            >>> hash(state1) == hash(state2)
            True
        """
        return hash(self.name)

    def __repr__(self) -> str:
        """Retourne une représentation technique de l'état.

        :return: Représentation du state sous forme de chaîne.
        :rtype: str

        :Example:
            >>> state = State("START", is_final=True)
            >>> repr(state)
            "State('START', is_final=True)"
        """
        return f"State({self.name!r}, is_final={self.is_final})"
