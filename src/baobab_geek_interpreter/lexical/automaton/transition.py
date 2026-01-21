"""Module contenant la classe Transition et les fonctions de condition pour les automates."""

from typing import Callable

from baobab_geek_interpreter.lexical.automaton.state import State


class Transition:
    """Représente une transition conditionnelle entre deux états.

    Une transition relie un état source à un état destination et est activée
    si la condition est satisfaite pour le caractère d'entrée.

    :param from_state: État source de la transition.
    :type from_state: State
    :param to_state: État destination de la transition.
    :type to_state: State
    :param condition: Fonction qui teste si un caractère active la transition.
    :type condition: Callable[[str], bool]

    :ivar from_state: État source.
    :type from_state: State
    :ivar to_state: État destination.
    :type to_state: State
    :ivar condition: Fonction de condition.
    :type condition: Callable[[str], bool]

    :Example:
        >>> start = State("START")
        >>> digit = State("DIGIT", is_final=True)
        >>> transition = Transition(start, digit, is_digit)
        >>> transition.can_transition('5')
        True
        >>> transition.can_transition('a')
        False
    """

    def __init__(
        self,
        from_state: State,
        to_state: State,
        condition: Callable[[str], bool],
    ) -> None:
        """Initialise une transition.

        :param from_state: État source de la transition.
        :type from_state: State
        :param to_state: État destination de la transition.
        :type to_state: State
        :param condition: Fonction qui teste si un caractère active la transition.
        :type condition: Callable[[str], bool]
        """
        self.from_state: State = from_state
        self.to_state: State = to_state
        self.condition: Callable[[str], bool] = condition

    def can_transition(self, char: str) -> bool:
        """Teste si le caractère active la transition.

        :param char: Caractère d'entrée à tester.
        :type char: str
        :return: True si la transition est activée, False sinon.
        :rtype: bool

        :Example:
            >>> start = State("START")
            >>> digit = State("DIGIT")
            >>> t = Transition(start, digit, is_digit)
            >>> t.can_transition('7')
            True
        """
        return self.condition(char)

    def __repr__(self) -> str:
        """Retourne une représentation technique de la transition.

        :return: Représentation de la transition sous forme de chaîne.
        :rtype: str

        :Example:
            >>> start = State("START")
            >>> end = State("END")
            >>> t = Transition(start, end, is_digit)
            >>> repr(t)
            "Transition(START -> END)"
        """
        return f"Transition({self.from_state.name} -> {self.to_state.name})"


# Fonctions de condition communes


def is_digit(char: str) -> bool:
    """Vérifie si le caractère est un chiffre (0-9).

    :param char: Caractère à tester.
    :type char: str
    :return: True si le caractère est un chiffre, False sinon.
    :rtype: bool

    :Example:
        >>> is_digit('5')
        True
        >>> is_digit('a')
        False
    """
    return char.isdigit()


def is_letter(char: str) -> bool:
    """Vérifie si le caractère est une lettre (a-z, A-Z).

    :param char: Caractère à tester.
    :type char: str
    :return: True si le caractère est une lettre, False sinon.
    :rtype: bool

    :Example:
        >>> is_letter('a')
        True
        >>> is_letter('5')
        False
    """
    return char.isalpha()


def is_alpha_numeric(char: str) -> bool:
    """Vérifie si le caractère est alphanumérique.

    :param char: Caractère à tester.
    :type char: str
    :return: True si le caractère est alphanumérique, False sinon.
    :rtype: bool

    :Example:
        >>> is_alpha_numeric('a')
        True
        >>> is_alpha_numeric('5')
        True
        >>> is_alpha_numeric('_')
        False
    """
    return char.isalnum()


def is_specific(target: str) -> Callable[[str], bool]:
    """Crée une condition pour un caractère spécifique.

    :param target: Caractère cible.
    :type target: str
    :return: Fonction de condition.
    :rtype: Callable[[str], bool]

    :Example:
        >>> dot_condition = is_specific('.')
        >>> dot_condition('.')
        True
        >>> dot_condition('a')
        False
    """
    return lambda char: char == target


def is_in_set(charset: str) -> Callable[[str], bool]:
    """Crée une condition pour un ensemble de caractères.

    :param charset: Chaîne contenant les caractères autorisés.
    :type charset: str
    :return: Fonction de condition.
    :rtype: Callable[[str], bool]

    :Example:
        >>> sign_condition = is_in_set('+-')
        >>> sign_condition('+')
        True
        >>> sign_condition('-')
        True
        >>> sign_condition('a')
        False
    """
    return lambda char: char in charset


def is_underscore(char: str) -> bool:
    """Vérifie si le caractère est un underscore (_).

    :param char: Caractère à tester.
    :type char: str
    :return: True si le caractère est un underscore, False sinon.
    :rtype: bool

    :Example:
        >>> is_underscore('_')
        True
        >>> is_underscore('a')
        False
    """
    return char == "_"


def is_letter_or_underscore(char: str) -> bool:
    """Vérifie si le caractère est une lettre ou un underscore.

    :param char: Caractère à tester.
    :type char: str
    :return: True si le caractère est une lettre ou un underscore, False sinon.
    :rtype: bool

    :Example:
        >>> is_letter_or_underscore('a')
        True
        >>> is_letter_or_underscore('_')
        True
        >>> is_letter_or_underscore('5')
        False
    """
    return is_letter(char) or is_underscore(char)


def is_alpha_numeric_or_underscore(char: str) -> bool:
    """Vérifie si le caractère est alphanumérique ou un underscore.

    :param char: Caractère à tester.
    :type char: str
    :return: True si le caractère est alphanumérique ou un underscore, False sinon.
    :rtype: bool

    :Example:
        >>> is_alpha_numeric_or_underscore('a')
        True
        >>> is_alpha_numeric_or_underscore('5')
        True
        >>> is_alpha_numeric_or_underscore('_')
        True
        >>> is_alpha_numeric_or_underscore('-')
        False
    """
    return is_alpha_numeric(char) or is_underscore(char)
