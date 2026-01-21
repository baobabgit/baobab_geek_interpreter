"""Tests unitaires pour la classe BaobabLexicalAnalyserException."""

import pytest

from baobab_geek_interpreter.exceptions.base_exception import (
    BaobabGeekInterpreterException,
)
from baobab_geek_interpreter.exceptions.lexical_exception import (
    BaobabLexicalAnalyserException,
)


class TestBaobabLexicalAnalyserException:
    """Classe de tests pour BaobabLexicalAnalyserException."""

    def test_inherits_from_base_exception(self) -> None:
        """Test que la classe hérite de BaobabGeekInterpreterException."""
        exception = BaobabLexicalAnalyserException("Test error")

        assert isinstance(exception, BaobabGeekInterpreterException)
        assert isinstance(exception, Exception)

    def test_init_with_message_only(self) -> None:
        """Test l'initialisation avec uniquement un message."""
        message = "Lexical error"
        exception = BaobabLexicalAnalyserException(message)

        assert exception.message == message
        assert exception.source is None
        assert exception.position is None
        assert exception.line is None
        assert exception.column is None

    def test_init_with_all_parameters(self) -> None:
        """Test l'initialisation avec tous les paramètres."""
        message = "Chaîne non fermée"
        source = 'service("test'
        position = 12
        line = 1
        column = 13

        exception = BaobabLexicalAnalyserException(
            message=message, source=source, position=position, line=line, column=column
        )

        assert exception.message == message
        assert exception.source == source
        assert exception.position == position
        assert exception.line == line
        assert exception.column == column

    def test_can_be_raised_and_caught(self) -> None:
        """Test que l'exception peut être levée et attrapée."""
        with pytest.raises(BaobabLexicalAnalyserException) as exc_info:
            raise BaobabLexicalAnalyserException("Lexical error")

        assert exc_info.value.message == "Lexical error"

    def test_can_be_caught_as_base_exception(self) -> None:
        """Test que l'exception peut être attrapée comme BaobabGeekInterpreterException."""
        try:
            raise BaobabLexicalAnalyserException("Test")
        except BaobabGeekInterpreterException as e:
            assert isinstance(e, BaobabLexicalAnalyserException)
            assert str(e) == "Test"

    def test_str_representation(self) -> None:
        """Test la représentation en chaîne."""
        exception = BaobabLexicalAnalyserException(
            "Invalid character", line=5, column=10
        )

        assert str(exception) == "Invalid character at line 5, column 10"
