"""Tests d'intégration pour la classe Automaton avec des automates réalistes."""

import pytest

from baobab_geek_interpreter.lexical.automaton.automaton import Automaton
from baobab_geek_interpreter.lexical.automaton.state import State
from baobab_geek_interpreter.lexical.automaton.transition import (
    Transition,
    is_alpha_numeric_or_underscore,
    is_digit,
    is_in_set,
    is_letter_or_underscore,
    is_specific,
)


def create_integer_automaton() -> Automaton:
    """Crée un automate pour reconnaître les entiers positifs [0-9]+.

    :return: Automate configuré pour les entiers.
    :rtype: Automaton
    """
    start = State("START")
    digit = State("DIGIT", is_final=True)

    automaton = Automaton(start)
    automaton.add_state(start)
    automaton.add_state(digit)
    automaton.set_final_state(digit)

    automaton.add_transition(Transition(start, digit, is_digit))
    automaton.add_transition(Transition(digit, digit, is_digit))

    return automaton


def create_identifier_automaton() -> Automaton:
    """Crée un automate pour reconnaître les identifiants [a-zA-Z_][a-zA-Z0-9_]*.

    :return: Automate configuré pour les identifiants.
    :rtype: Automaton
    """
    start = State("START")
    first_char = State("FIRST_CHAR", is_final=True)

    automaton = Automaton(start)
    automaton.add_state(start)
    automaton.add_state(first_char)
    automaton.set_final_state(first_char)

    automaton.add_transition(Transition(start, first_char, is_letter_or_underscore))
    automaton.add_transition(Transition(first_char, first_char, is_alpha_numeric_or_underscore))

    return automaton


def create_signed_integer_automaton() -> Automaton:
    """Crée un automate pour reconnaître les entiers signés -?[0-9]+.

    :return: Automate configuré pour les entiers signés.
    :rtype: Automaton
    """
    start = State("START")
    sign = State("SIGN")
    digit = State("DIGIT", is_final=True)

    automaton = Automaton(start)
    automaton.add_state(start)
    automaton.add_state(sign)
    automaton.add_state(digit)
    automaton.set_final_state(digit)

    automaton.add_transition(Transition(start, sign, is_specific("-")))
    automaton.add_transition(Transition(start, digit, is_digit))
    automaton.add_transition(Transition(sign, digit, is_digit))
    automaton.add_transition(Transition(digit, digit, is_digit))

    return automaton


def create_keyword_automaton(keyword: str) -> Automaton:
    """Crée un automate pour reconnaître un mot-clé spécifique.

    :param keyword: Mot-clé à reconnaître.
    :type keyword: str
    :return: Automate configuré pour le mot-clé.
    :rtype: Automaton
    """
    states = []
    start = State("START")
    automaton = Automaton(start)
    automaton.add_state(start)

    current_state = start

    for i, char in enumerate(keyword):
        is_last = i == len(keyword) - 1
        next_state = State(f"CHAR_{i}", is_final=is_last)
        automaton.add_state(next_state)

        if is_last:
            automaton.set_final_state(next_state)

        automaton.add_transition(Transition(current_state, next_state, is_specific(char)))
        current_state = next_state

    return automaton


class TestIntegerAutomaton:
    """Tests pour l'automate d'entiers positifs."""

    def test_accepts_single_digit(self) -> None:
        """Test l'acceptation d'un chiffre unique."""
        automaton = create_integer_automaton()
        assert automaton.process("0") is True
        assert automaton.process("5") is True
        assert automaton.process("9") is True

    def test_accepts_multiple_digits(self) -> None:
        """Test l'acceptation de plusieurs chiffres."""
        automaton = create_integer_automaton()
        assert automaton.process("123") is True
        assert automaton.process("999999") is True

    def test_rejects_letters(self) -> None:
        """Test le rejet des lettres."""
        automaton = create_integer_automaton()
        assert automaton.process("abc") is False
        assert automaton.process("12a34") is False

    def test_rejects_empty_string(self) -> None:
        """Test le rejet d'une chaîne vide."""
        automaton = create_integer_automaton()
        assert automaton.process("") is False


class TestIdentifierAutomaton:
    """Tests pour l'automate d'identifiants."""

    def test_accepts_simple_identifier(self) -> None:
        """Test l'acceptation d'un identifiant simple."""
        automaton = create_identifier_automaton()
        assert automaton.process("variable") is True
        assert automaton.process("myVar") is True

    def test_accepts_identifier_with_underscore(self) -> None:
        """Test l'acceptation d'identifiants avec underscore."""
        automaton = create_identifier_automaton()
        assert automaton.process("_private") is True
        assert automaton.process("my_var") is True

    def test_accepts_identifier_with_digits(self) -> None:
        """Test l'acceptation d'identifiants avec chiffres."""
        automaton = create_identifier_automaton()
        assert automaton.process("var123") is True
        assert automaton.process("CamelCase123") is True

    def test_accepts_single_letter(self) -> None:
        """Test l'acceptation d'une seule lettre."""
        automaton = create_identifier_automaton()
        assert automaton.process("a") is True
        assert automaton.process("Z") is True

    def test_accepts_single_underscore(self) -> None:
        """Test l'acceptation d'un underscore seul."""
        automaton = create_identifier_automaton()
        assert automaton.process("_") is True

    def test_rejects_starting_with_digit(self) -> None:
        """Test le rejet d'identifiants commençant par un chiffre."""
        automaton = create_identifier_automaton()
        assert automaton.process("123abc") is False

    def test_rejects_special_characters(self) -> None:
        """Test le rejet de caractères spéciaux."""
        automaton = create_identifier_automaton()
        assert automaton.process("my-var") is False
        assert automaton.process("var.name") is False

    def test_rejects_empty_string(self) -> None:
        """Test le rejet d'une chaîne vide."""
        automaton = create_identifier_automaton()
        assert automaton.process("") is False


class TestSignedIntegerAutomaton:
    """Tests pour l'automate d'entiers signés."""

    def test_accepts_positive_integer(self) -> None:
        """Test l'acceptation d'un entier positif."""
        automaton = create_signed_integer_automaton()
        assert automaton.process("123") is True
        assert automaton.process("0") is True

    def test_accepts_negative_integer(self) -> None:
        """Test l'acceptation d'un entier négatif."""
        automaton = create_signed_integer_automaton()
        assert automaton.process("-123") is True
        assert automaton.process("-456") is True

    def test_rejects_sign_without_digit(self) -> None:
        """Test le rejet d'un signe sans chiffre."""
        automaton = create_signed_integer_automaton()
        assert automaton.process("-") is False

    def test_rejects_double_sign(self) -> None:
        """Test le rejet d'un double signe."""
        automaton = create_signed_integer_automaton()
        assert automaton.process("--1") is False
        assert automaton.process("+-1") is False

    def test_rejects_empty_string(self) -> None:
        """Test le rejet d'une chaîne vide."""
        automaton = create_signed_integer_automaton()
        assert automaton.process("") is False


class TestKeywordAutomaton:
    """Tests pour l'automate de mots-clés."""

    def test_accepts_exact_keyword(self) -> None:
        """Test l'acceptation du mot-clé exact."""
        automaton = create_keyword_automaton("if")
        assert automaton.process("if") is True

    def test_rejects_partial_keyword(self) -> None:
        """Test le rejet d'un mot-clé partiel."""
        automaton = create_keyword_automaton("if")
        assert automaton.process("i") is False

    def test_rejects_keyword_with_extra_chars(self) -> None:
        """Test le rejet d'un mot-clé avec des caractères supplémentaires."""
        automaton = create_keyword_automaton("if")
        assert automaton.process("iff") is False

    def test_rejects_wrong_case(self) -> None:
        """Test le rejet d'un mot-clé avec une casse différente."""
        automaton = create_keyword_automaton("if")
        assert automaton.process("IF") is False
        assert automaton.process("If") is False

    def test_accepts_longer_keyword(self) -> None:
        """Test l'acceptation d'un mot-clé plus long."""
        automaton = create_keyword_automaton("while")
        assert automaton.process("while") is True

    def test_rejects_empty_string(self) -> None:
        """Test le rejet d'une chaîne vide."""
        automaton = create_keyword_automaton("if")
        assert automaton.process("") is False


class TestComplexScenarios:
    """Tests de scénarios complexes."""

    def test_automaton_can_be_reused(self) -> None:
        """Test qu'un automate peut être réutilisé plusieurs fois."""
        automaton = create_integer_automaton()

        assert automaton.process("123") is True
        assert automaton.process("456") is True
        assert automaton.process("abc") is False
        assert automaton.process("789") is True

    def test_different_automata_are_independent(self) -> None:
        """Test que différents automates sont indépendants."""
        int_automaton = create_integer_automaton()
        id_automaton = create_identifier_automaton()

        assert int_automaton.process("123") is True
        assert id_automaton.process("123") is False

        assert int_automaton.process("abc") is False
        assert id_automaton.process("abc") is True
