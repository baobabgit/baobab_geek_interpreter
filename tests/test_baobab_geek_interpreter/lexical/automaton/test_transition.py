"""Tests unitaires pour la classe Transition et les fonctions de condition."""

import pytest

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


class TestTransition:
    """Classe de tests pour Transition."""

    def test_transition_creation(self) -> None:
        """Test la création d'une transition simple."""
        start = State("START")
        end = State("END")
        transition = Transition(start, end, is_digit)

        assert transition.from_state == start
        assert transition.to_state == end
        assert transition.condition == is_digit

    def test_can_transition_returns_true_when_condition_met(self) -> None:
        """Test que can_transition retourne True si la condition est satisfaite."""
        start = State("START")
        end = State("END")
        transition = Transition(start, end, is_digit)

        assert transition.can_transition("5") is True

    def test_can_transition_returns_false_when_condition_not_met(self) -> None:
        """Test que can_transition retourne False si la condition n'est pas satisfaite."""
        start = State("START")
        end = State("END")
        transition = Transition(start, end, is_digit)

        assert transition.can_transition("a") is False

    def test_transition_with_lambda(self) -> None:
        """Test une transition avec une lambda personnalisée."""
        start = State("START")
        end = State("END")
        transition = Transition(start, end, lambda c: c in "abc")

        assert transition.can_transition("a") is True
        assert transition.can_transition("b") is True
        assert transition.can_transition("d") is False

    def test_transition_repr(self) -> None:
        """Test la représentation __repr__ d'une transition."""
        start = State("START")
        end = State("END")
        transition = Transition(start, end, is_digit)

        assert repr(transition) == "Transition(START -> END)"


class TestIsDigit:
    """Tests pour la fonction is_digit."""

    def test_is_digit_with_digit(self) -> None:
        """Test is_digit avec un chiffre."""
        assert is_digit("0") is True
        assert is_digit("5") is True
        assert is_digit("9") is True

    def test_is_digit_with_letter(self) -> None:
        """Test is_digit avec une lettre."""
        assert is_digit("a") is False
        assert is_digit("Z") is False

    def test_is_digit_with_special_char(self) -> None:
        """Test is_digit avec un caractère spécial."""
        assert is_digit(".") is False
        assert is_digit("-") is False


class TestIsLetter:
    """Tests pour la fonction is_letter."""

    def test_is_letter_with_lowercase(self) -> None:
        """Test is_letter avec des minuscules."""
        assert is_letter("a") is True
        assert is_letter("z") is True

    def test_is_letter_with_uppercase(self) -> None:
        """Test is_letter avec des majuscules."""
        assert is_letter("A") is True
        assert is_letter("Z") is True

    def test_is_letter_with_digit(self) -> None:
        """Test is_letter avec un chiffre."""
        assert is_letter("0") is False
        assert is_letter("9") is False

    def test_is_letter_with_special_char(self) -> None:
        """Test is_letter avec un caractère spécial."""
        assert is_letter("_") is False
        assert is_letter(".") is False


class TestIsAlphaNumeric:
    """Tests pour la fonction is_alpha_numeric."""

    def test_is_alpha_numeric_with_letter(self) -> None:
        """Test is_alpha_numeric avec une lettre."""
        assert is_alpha_numeric("a") is True
        assert is_alpha_numeric("Z") is True

    def test_is_alpha_numeric_with_digit(self) -> None:
        """Test is_alpha_numeric avec un chiffre."""
        assert is_alpha_numeric("0") is True
        assert is_alpha_numeric("9") is True

    def test_is_alpha_numeric_with_special_char(self) -> None:
        """Test is_alpha_numeric avec un caractère spécial."""
        assert is_alpha_numeric("_") is False
        assert is_alpha_numeric(".") is False


class TestIsSpecific:
    """Tests pour la fonction is_specific."""

    def test_is_specific_with_match(self) -> None:
        """Test is_specific avec un caractère correspondant."""
        dot_condition = is_specific(".")
        assert dot_condition(".") is True

    def test_is_specific_with_no_match(self) -> None:
        """Test is_specific avec un caractère non correspondant."""
        dot_condition = is_specific(".")
        assert dot_condition("a") is False
        assert dot_condition(",") is False

    def test_is_specific_with_different_targets(self) -> None:
        """Test is_specific avec différents caractères cibles."""
        minus_condition = is_specific("-")
        plus_condition = is_specific("+")

        assert minus_condition("-") is True
        assert minus_condition("+") is False
        assert plus_condition("+") is True
        assert plus_condition("-") is False


class TestIsInSet:
    """Tests pour la fonction is_in_set."""

    def test_is_in_set_with_match(self) -> None:
        """Test is_in_set avec un caractère dans l'ensemble."""
        sign_condition = is_in_set("+-")
        assert sign_condition("+") is True
        assert sign_condition("-") is True

    def test_is_in_set_with_no_match(self) -> None:
        """Test is_in_set avec un caractère hors de l'ensemble."""
        sign_condition = is_in_set("+-")
        assert sign_condition("a") is False
        assert sign_condition("5") is False

    def test_is_in_set_with_empty_set(self) -> None:
        """Test is_in_set avec un ensemble vide."""
        empty_condition = is_in_set("")
        assert empty_condition("a") is False
        assert empty_condition("5") is False


class TestIsUnderscore:
    """Tests pour la fonction is_underscore."""

    def test_is_underscore_with_underscore(self) -> None:
        """Test is_underscore avec un underscore."""
        assert is_underscore("_") is True

    def test_is_underscore_with_letter(self) -> None:
        """Test is_underscore avec une lettre."""
        assert is_underscore("a") is False

    def test_is_underscore_with_digit(self) -> None:
        """Test is_underscore avec un chiffre."""
        assert is_underscore("5") is False


class TestIsLetterOrUnderscore:
    """Tests pour la fonction is_letter_or_underscore."""

    def test_is_letter_or_underscore_with_letter(self) -> None:
        """Test is_letter_or_underscore avec une lettre."""
        assert is_letter_or_underscore("a") is True
        assert is_letter_or_underscore("Z") is True

    def test_is_letter_or_underscore_with_underscore(self) -> None:
        """Test is_letter_or_underscore avec un underscore."""
        assert is_letter_or_underscore("_") is True

    def test_is_letter_or_underscore_with_digit(self) -> None:
        """Test is_letter_or_underscore avec un chiffre."""
        assert is_letter_or_underscore("5") is False

    def test_is_letter_or_underscore_with_special_char(self) -> None:
        """Test is_letter_or_underscore avec un caractère spécial."""
        assert is_letter_or_underscore(".") is False


class TestIsAlphaNumericOrUnderscore:
    """Tests pour la fonction is_alpha_numeric_or_underscore."""

    def test_is_alpha_numeric_or_underscore_with_letter(self) -> None:
        """Test is_alpha_numeric_or_underscore avec une lettre."""
        assert is_alpha_numeric_or_underscore("a") is True
        assert is_alpha_numeric_or_underscore("Z") is True

    def test_is_alpha_numeric_or_underscore_with_digit(self) -> None:
        """Test is_alpha_numeric_or_underscore avec un chiffre."""
        assert is_alpha_numeric_or_underscore("0") is True
        assert is_alpha_numeric_or_underscore("9") is True

    def test_is_alpha_numeric_or_underscore_with_underscore(self) -> None:
        """Test is_alpha_numeric_or_underscore avec un underscore."""
        assert is_alpha_numeric_or_underscore("_") is True

    def test_is_alpha_numeric_or_underscore_with_special_char(self) -> None:
        """Test is_alpha_numeric_or_underscore avec un caractère spécial."""
        assert is_alpha_numeric_or_underscore(".") is False
        assert is_alpha_numeric_or_underscore("-") is False
