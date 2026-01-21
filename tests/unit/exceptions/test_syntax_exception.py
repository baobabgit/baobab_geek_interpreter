"""Tests unitaires pour la classe BaobabSyntaxAnalyserException."""

import pytest

from baobab_geek_interpreter.exceptions.base_exception import (
    BaobabGeekInterpreterException,
)
from baobab_geek_interpreter.exceptions.syntax_exception import (
    BaobabSyntaxAnalyserException,
)


class TestBaobabSyntaxAnalyserException:
    """Classe de tests pour BaobabSyntaxAnalyserException."""

    def test_inherits_from_base_exception(self) -> None:
        """Test que la classe hérite de BaobabGeekInterpreterException."""
        exception = BaobabSyntaxAnalyserException("Test error")

        assert isinstance(exception, BaobabGeekInterpreterException)
        assert isinstance(exception, Exception)

    def test_init_with_message_only(self) -> None:
        """Test l'initialisation avec uniquement un message."""
        message = "Syntax error"
        exception = BaobabSyntaxAnalyserException(message)

        assert exception.message == message
        assert exception.source is None
        assert exception.position is None
        assert exception.line is None
        assert exception.column is None

    def test_init_with_all_parameters(self) -> None:
        """Test l'initialisation avec tous les paramètres."""
        message = "Token inattendu"
        source = "service(1, 2"
        position = 13
        line = 1
        column = 14

        exception = BaobabSyntaxAnalyserException(
            message=message, source=source, position=position, line=line, column=column
        )

        assert exception.message == message
        assert exception.source == source
        assert exception.position == position
        assert exception.line == line
        assert exception.column == column

    def test_can_be_raised_and_caught(self) -> None:
        """Test que l'exception peut être levée et attrapée."""
        with pytest.raises(BaobabSyntaxAnalyserException) as exc_info:
            raise BaobabSyntaxAnalyserException("Syntax error")

        assert exc_info.value.message == "Syntax error"

    def test_can_be_caught_as_base_exception(self) -> None:
        """Test que l'exception peut être attrapée comme BaobabGeekInterpreterException."""
        try:
            raise BaobabSyntaxAnalyserException("Test")
        except BaobabGeekInterpreterException as e:
            assert isinstance(e, BaobabSyntaxAnalyserException)
            assert str(e) == "Test"

    def test_str_representation(self) -> None:
        """Test la représentation en chaîne."""
        exception = BaobabSyntaxAnalyserException(
            "Missing parenthesis", line=3, column=7
        )

        assert str(exception) == "Missing parenthesis at line 3, column 7"
