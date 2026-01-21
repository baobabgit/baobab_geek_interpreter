"""Tests unitaires pour la classe State."""

import pytest

from baobab_geek_interpreter.lexical.automaton.state import State


class TestState:
    """Classe de tests pour State."""

    def test_state_creation_simple(self) -> None:
        """Test la création d'un état simple."""
        state = State("START")
        assert state.name == "START"
        assert state.is_final is False

    def test_state_creation_with_is_final(self) -> None:
        """Test la création d'un état final."""
        state = State("END", is_final=True)
        assert state.name == "END"
        assert state.is_final is True

    def test_state_equality_same_name(self) -> None:
        """Test l'égalité entre deux états avec le même nom."""
        state1 = State("START")
        state2 = State("START")
        assert state1 == state2

    def test_state_equality_different_name(self) -> None:
        """Test l'inégalité entre deux états avec des noms différents."""
        state1 = State("START")
        state2 = State("END")
        assert state1 != state2

    def test_state_equality_with_non_state(self) -> None:
        """Test la comparaison avec un objet qui n'est pas un State."""
        state = State("START")
        assert state != "START"
        assert state != 123
        assert state != None

    def test_state_hash_consistency(self) -> None:
        """Test que le hash est cohérent pour des états égaux."""
        state1 = State("START")
        state2 = State("START")
        assert hash(state1) == hash(state2)

    def test_state_hash_different_for_different_names(self) -> None:
        """Test que le hash est différent pour des noms différents."""
        state1 = State("START")
        state2 = State("END")
        # Note: techniquement, les hashs peuvent être égaux (collision),
        # mais c'est extrêmement improbable pour des noms différents
        assert hash(state1) != hash(state2)

    def test_state_can_be_used_in_set(self) -> None:
        """Test que les états peuvent être utilisés dans un set."""
        state1 = State("START")
        state2 = State("START")
        state3 = State("END")

        states = {state1, state2, state3}
        assert len(states) == 2  # state1 et state2 sont identiques

    def test_state_can_be_used_as_dict_key(self) -> None:
        """Test que les états peuvent être utilisés comme clés de dictionnaire."""
        state1 = State("START")
        state2 = State("END")

        d = {state1: "début", state2: "fin"}
        assert d[state1] == "début"
        assert d[state2] == "fin"

    def test_state_repr(self) -> None:
        """Test la représentation __repr__ d'un état."""
        state = State("START", is_final=False)
        assert repr(state) == "State('START', is_final=False)"

    def test_state_repr_final(self) -> None:
        """Test la représentation __repr__ d'un état final."""
        state = State("END", is_final=True)
        assert repr(state) == "State('END', is_final=True)"

    def test_state_with_empty_name(self) -> None:
        """Test la création d'un état avec un nom vide."""
        state = State("")
        assert state.name == ""
        assert state.is_final is False

    def test_state_with_special_characters_in_name(self) -> None:
        """Test la création d'un état avec des caractères spéciaux dans le nom."""
        state = State("STATE_123")
        assert state.name == "STATE_123"

    def test_state_is_final_can_be_modified(self) -> None:
        """Test que l'attribut is_final peut être modifié."""
        state = State("START", is_final=False)
        assert state.is_final is False
        state.is_final = True
        assert state.is_final is True

    def test_state_name_can_be_modified(self) -> None:
        """Test que l'attribut name peut être modifié (mais déconseillé)."""
        state = State("START")
        assert state.name == "START"
        state.name = "NEW_START"
        assert state.name == "NEW_START"
