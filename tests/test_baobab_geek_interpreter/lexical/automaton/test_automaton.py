"""Tests unitaires pour la classe Automaton."""

import pytest

from baobab_geek_interpreter.lexical.automaton.automaton import Automaton
from baobab_geek_interpreter.lexical.automaton.state import State
from baobab_geek_interpreter.lexical.automaton.transition import (
    Transition,
    is_digit,
    is_letter,
)


class TestAutomaton:
    """Classe de tests pour Automaton."""

    def test_automaton_creation(self) -> None:
        """Test la création d'un automate simple."""
        start = State("START")
        automaton = Automaton(start)

        assert automaton.initial_state == start
        assert automaton.current_state == start
        assert len(automaton.states) == 0
        assert len(automaton.transitions) == 0
        assert len(automaton.final_states) == 0

    def test_add_state(self) -> None:
        """Test l'ajout d'un état."""
        start = State("START")
        end = State("END")
        automaton = Automaton(start)

        automaton.add_state(start)
        automaton.add_state(end)

        assert len(automaton.states) == 2
        assert start in automaton.states
        assert end in automaton.states

    def test_add_state_duplicate_raises_error(self) -> None:
        """Test que l'ajout d'un état en double lève une exception."""
        start = State("START")
        automaton = Automaton(start)

        automaton.add_state(start)

        with pytest.raises(ValueError, match="existe déjà"):
            automaton.add_state(start)

    def test_add_transition(self) -> None:
        """Test l'ajout d'une transition."""
        start = State("START")
        end = State("END")
        automaton = Automaton(start)

        automaton.add_state(start)
        automaton.add_state(end)

        transition = Transition(start, end, is_digit)
        automaton.add_transition(transition)

        assert len(automaton.transitions) == 1
        assert transition in automaton.transitions

    def test_add_transition_with_missing_from_state_raises_error(self) -> None:
        """Test qu'une transition avec état source manquant lève une exception."""
        start = State("START")
        end = State("END")
        automaton = Automaton(start)

        automaton.add_state(end)

        transition = Transition(start, end, is_digit)

        with pytest.raises(ValueError, match="état source.*n'existe pas"):
            automaton.add_transition(transition)

    def test_add_transition_with_missing_to_state_raises_error(self) -> None:
        """Test qu'une transition avec état destination manquant lève une exception."""
        start = State("START")
        end = State("END")
        automaton = Automaton(start)

        automaton.add_state(start)

        transition = Transition(start, end, is_digit)

        with pytest.raises(ValueError, match="état destination.*n'existe pas"):
            automaton.add_transition(transition)

    def test_set_final_state(self) -> None:
        """Test la définition d'un état final."""
        start = State("START")
        end = State("END")
        automaton = Automaton(start)

        automaton.add_state(start)
        automaton.add_state(end)
        automaton.set_final_state(end)

        assert len(automaton.final_states) == 1
        assert end in automaton.final_states
        assert end.is_final is True

    def test_set_final_state_with_missing_state_raises_error(self) -> None:
        """Test que définir un état final inexistant lève une exception."""
        start = State("START")
        end = State("END")
        automaton = Automaton(start)

        automaton.add_state(start)

        with pytest.raises(ValueError, match="n'existe pas"):
            automaton.set_final_state(end)

    def test_reset(self) -> None:
        """Test que reset retourne à l'état initial."""
        start = State("START")
        digit = State("DIGIT")
        automaton = Automaton(start)

        automaton.add_state(start)
        automaton.add_state(digit)
        automaton.add_transition(Transition(start, digit, is_digit))

        # Change d'état
        automaton.step("5")
        assert automaton.current_state == digit

        # Reset
        automaton.reset()
        assert automaton.current_state == start

    def test_is_in_final_state(self) -> None:
        """Test la détection d'un état final."""
        start = State("START")
        end = State("END", is_final=True)
        automaton = Automaton(start)

        automaton.add_state(start)
        automaton.add_state(end)
        automaton.set_final_state(end)

        assert automaton.is_in_final_state() is False

        automaton.current_state = end
        assert automaton.is_in_final_state() is True

    def test_get_current_state(self) -> None:
        """Test la récupération de l'état courant."""
        start = State("START")
        automaton = Automaton(start)

        assert automaton.get_current_state() == start

    def test_step_with_valid_transition(self) -> None:
        """Test step avec une transition valide."""
        start = State("START")
        digit = State("DIGIT")
        automaton = Automaton(start)

        automaton.add_state(start)
        automaton.add_state(digit)
        automaton.add_transition(Transition(start, digit, is_digit))

        result = automaton.step("5")

        assert result is True
        assert automaton.current_state == digit

    def test_step_with_invalid_transition(self) -> None:
        """Test step sans transition valide."""
        start = State("START")
        digit = State("DIGIT")
        automaton = Automaton(start)

        automaton.add_state(start)
        automaton.add_state(digit)
        automaton.add_transition(Transition(start, digit, is_digit))

        result = automaton.step("a")

        assert result is False
        assert automaton.current_state == start  # Reste dans le même état

    def test_process_accepts_valid_string(self) -> None:
        """Test process accepte une chaîne valide."""
        start = State("START")
        digit = State("DIGIT", is_final=True)
        automaton = Automaton(start)

        automaton.add_state(start)
        automaton.add_state(digit)
        automaton.set_final_state(digit)
        automaton.add_transition(Transition(start, digit, is_digit))
        automaton.add_transition(Transition(digit, digit, is_digit))

        assert automaton.process("123") is True

    def test_process_rejects_invalid_string(self) -> None:
        """Test process rejette une chaîne invalide."""
        start = State("START")
        digit = State("DIGIT", is_final=True)
        automaton = Automaton(start)

        automaton.add_state(start)
        automaton.add_state(digit)
        automaton.set_final_state(digit)
        automaton.add_transition(Transition(start, digit, is_digit))
        automaton.add_transition(Transition(digit, digit, is_digit))

        assert automaton.process("abc") is False

    def test_process_rejects_empty_string_if_initial_not_final(self) -> None:
        """Test process rejette une chaîne vide si l'état initial n'est pas final."""
        start = State("START")
        digit = State("DIGIT", is_final=True)
        automaton = Automaton(start)

        automaton.add_state(start)
        automaton.add_state(digit)
        automaton.set_final_state(digit)

        assert automaton.process("") is False

    def test_process_accepts_empty_string_if_initial_is_final(self) -> None:
        """Test process accepte une chaîne vide si l'état initial est final."""
        start = State("START", is_final=True)
        automaton = Automaton(start)

        automaton.add_state(start)
        automaton.set_final_state(start)

        assert automaton.process("") is True

    def test_process_resets_before_execution(self) -> None:
        """Test que process réinitialise l'automate avant l'exécution."""
        start = State("START")
        digit = State("DIGIT", is_final=True)
        automaton = Automaton(start)

        automaton.add_state(start)
        automaton.add_state(digit)
        automaton.set_final_state(digit)
        automaton.add_transition(Transition(start, digit, is_digit))
        automaton.add_transition(Transition(digit, digit, is_digit))

        # Premier traitement
        automaton.process("123")
        assert automaton.current_state == digit

        # Deuxième traitement (doit reset automatiquement)
        result = automaton.process("456")
        assert result is True

    def test_multiple_transitions_from_same_state(self) -> None:
        """Test avec plusieurs transitions depuis le même état."""
        start = State("START")
        digit = State("DIGIT", is_final=True)
        letter = State("LETTER", is_final=True)
        automaton = Automaton(start)

        automaton.add_state(start)
        automaton.add_state(digit)
        automaton.add_state(letter)
        automaton.set_final_state(digit)
        automaton.set_final_state(letter)

        automaton.add_transition(Transition(start, digit, is_digit))
        automaton.add_transition(Transition(start, letter, is_letter))

        assert automaton.process("5") is True
        assert automaton.process("a") is True
        assert automaton.process(".") is False
