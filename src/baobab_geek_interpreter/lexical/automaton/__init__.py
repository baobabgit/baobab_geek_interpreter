"""Module d'automates finis déterministes pour l'analyse lexicale.

Ce module fournit les classes nécessaires pour construire et exécuter
des automates finis déterministes (AFD) utilisés dans l'analyse lexicale.

:Example:
    >>> from baobab_geek_interpreter.lexical.automaton import State, Transition, Automaton
    >>> start = State("START")
    >>> digit = State("DIGIT", is_final=True)
    >>> automaton = Automaton(start)
    >>> automaton.add_state(start)
    >>> automaton.add_state(digit)
    >>> automaton.set_final_state(digit)
"""

from baobab_geek_interpreter.lexical.automaton.automaton import Automaton
from baobab_geek_interpreter.lexical.automaton.state import State
from baobab_geek_interpreter.lexical.automaton.transition import (
    Transition,
    is_alpha_numeric,
    is_alpha_numeric_or_underscore,
    is_digit,
    is_in_set,
    is_letter,
    is_letter_or_underscore,
    is_specific,
    is_underscore,
)

__all__ = [
    "Automaton",
    "State",
    "Transition",
    "is_alpha_numeric",
    "is_alpha_numeric_or_underscore",
    "is_digit",
    "is_in_set",
    "is_letter",
    "is_letter_or_underscore",
    "is_specific",
    "is_underscore",
]
