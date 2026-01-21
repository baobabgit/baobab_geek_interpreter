"""Module contenant la classe Automaton pour les automates finis déterministes."""

from typing import List, Optional, Set

from baobab_geek_interpreter.lexical.automaton.state import State
from baobab_geek_interpreter.lexical.automaton.transition import Transition


class Automaton:
    """Représente un automate fini déterministe (AFD).

    Un automate est composé d'un ensemble d'états, d'un état initial,
    d'états finaux et de transitions. Il peut traiter une chaîne d'entrée
    et déterminer si elle est acceptée ou rejetée.

    :param initial_state: État de départ de l'automate.
    :type initial_state: State

    :ivar states: Ensemble de tous les états de l'automate.
    :type states: Set[State]
    :ivar initial_state: État de départ.
    :type initial_state: State
    :ivar current_state: État courant pendant l'exécution.
    :type current_state: State
    :ivar transitions: Liste de toutes les transitions.
    :type transitions: List[Transition]
    :ivar final_states: Ensemble des états acceptants.
    :type final_states: Set[State]

    :Example:
        >>> start = State("START")
        >>> digit = State("DIGIT", is_final=True)
        >>> automaton = Automaton(start)
        >>> automaton.add_state(start)
        >>> automaton.add_state(digit)
        >>> automaton.set_final_state(digit)
        >>> automaton.process("123")
        True
    """

    def __init__(self, initial_state: State) -> None:
        """Initialise un automate avec un état initial.

        :param initial_state: État de départ de l'automate.
        :type initial_state: State
        """
        self.states: Set[State] = set()
        self.initial_state: State = initial_state
        self.current_state: State = initial_state
        self.transitions: List[Transition] = []
        self.final_states: Set[State] = set()

    def add_state(self, state: State) -> None:
        """Ajoute un état à l'automate.

        :param state: État à ajouter.
        :type state: State
        :raises ValueError: Si l'état existe déjà dans l'automate.

        :Example:
            >>> automaton = Automaton(State("START"))
            >>> automaton.add_state(State("END"))
        """
        if state in self.states:
            raise ValueError(f"L'état '{state.name}' existe déjà dans l'automate")
        self.states.add(state)

    def add_transition(self, transition: Transition) -> None:
        """Ajoute une transition à l'automate.

        :param transition: Transition à ajouter.
        :type transition: Transition
        :raises ValueError: Si les états source ou destination n'existent pas.

        :Example:
            >>> start = State("START")
            >>> end = State("END")
            >>> automaton = Automaton(start)
            >>> automaton.add_state(start)
            >>> automaton.add_state(end)
            >>> automaton.add_transition(Transition(start, end, is_digit))
        """
        if transition.from_state not in self.states:
            raise ValueError(
                f"L'état source '{transition.from_state.name}' " f"n'existe pas dans l'automate"
            )
        if transition.to_state not in self.states:
            raise ValueError(
                f"L'état destination '{transition.to_state.name}' " f"n'existe pas dans l'automate"
            )
        self.transitions.append(transition)

    def set_final_state(self, state: State) -> None:
        """Marque un état comme final (acceptant).

        :param state: État à marquer comme final.
        :type state: State
        :raises ValueError: Si l'état n'existe pas dans l'automate.

        :Example:
            >>> automaton = Automaton(State("START"))
            >>> end = State("END", is_final=True)
            >>> automaton.add_state(end)
            >>> automaton.set_final_state(end)
        """
        if state not in self.states:
            raise ValueError(f"L'état '{state.name}' n'existe pas dans l'automate")
        self.final_states.add(state)
        state.is_final = True

    def reset(self) -> None:
        """Réinitialise l'automate à l'état initial.

        :Example:
            >>> automaton = Automaton(State("START"))
            >>> automaton.step('a')
            >>> automaton.reset()
            >>> automaton.current_state == automaton.initial_state
            True
        """
        self.current_state = self.initial_state

    def is_in_final_state(self) -> bool:
        """Vérifie si l'état courant est un état final.

        :return: True si l'état courant est acceptant, False sinon.
        :rtype: bool

        :Example:
            >>> start = State("START")
            >>> end = State("END", is_final=True)
            >>> automaton = Automaton(start)
            >>> automaton.add_state(start)
            >>> automaton.add_state(end)
            >>> automaton.set_final_state(end)
            >>> automaton.is_in_final_state()
            False
        """
        return self.current_state in self.final_states

    def get_current_state(self) -> State:
        """Retourne l'état courant de l'automate.

        :return: État courant.
        :rtype: State

        :Example:
            >>> start = State("START")
            >>> automaton = Automaton(start)
            >>> automaton.get_current_state() == start
            True
        """
        return self.current_state

    def _find_transition(self, from_state: State, char: str) -> Optional[Transition]:
        """Cherche une transition applicable depuis un état pour un caractère.

        :param from_state: État source.
        :type from_state: State
        :param char: Caractère d'entrée.
        :type char: str
        :return: Transition applicable ou None si aucune n'est trouvée.
        :rtype: Optional[Transition]
        """
        for transition in self.transitions:
            if transition.from_state == from_state and transition.can_transition(char):
                return transition
        return None

    def step(self, char: str) -> bool:
        """Exécute un pas de l'automate pour un caractère.

        Change l'état courant si une transition applicable est trouvée.

        :param char: Caractère d'entrée.
        :type char: str
        :return: True si une transition a été trouvée, False sinon.
        :rtype: bool

        :Example:
            >>> start = State("START")
            >>> digit = State("DIGIT", is_final=True)
            >>> automaton = Automaton(start)
            >>> automaton.add_state(start)
            >>> automaton.add_state(digit)
            >>> from baobab_geek_interpreter.lexical.automaton.transition import is_digit
            >>> automaton.add_transition(Transition(start, digit, is_digit))
            >>> automaton.step('5')
            True
            >>> automaton.current_state == digit
            True
        """
        transition = self._find_transition(self.current_state, char)
        if transition is None:
            return False

        self.current_state = transition.to_state
        return True

    def process(self, input_string: str) -> bool:
        """Traite une chaîne d'entrée et retourne si elle est acceptée.

        L'automate est réinitialisé avant le traitement. La chaîne est acceptée
        si l'automate se termine dans un état final après avoir traité tous
        les caractères.

        :param input_string: Chaîne à traiter.
        :type input_string: str
        :return: True si la chaîne est acceptée, False sinon.
        :rtype: bool

        :Example:
            >>> start = State("START")
            >>> digit = State("DIGIT", is_final=True)
            >>> automaton = Automaton(start)
            >>> automaton.add_state(start)
            >>> automaton.add_state(digit)
            >>> automaton.set_final_state(digit)
            >>> from baobab_geek_interpreter.lexical.automaton.transition import is_digit
            >>> automaton.add_transition(Transition(start, digit, is_digit))
            >>> automaton.add_transition(Transition(digit, digit, is_digit))
            >>> automaton.process("123")
            True
            >>> automaton.process("abc")
            False
        """
        self.reset()

        for char in input_string:
            if not self.step(char):
                return False

        return self.is_in_final_state()
