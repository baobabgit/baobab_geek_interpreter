"""Tests unitaires pour la classe BaobabGeekInterpreterException."""

import pytest

from baobab_geek_interpreter.exceptions.base_exception import (
    BaobabGeekInterpreterException,
)


class TestBaobabGeekInterpreterException:
    """Classe de tests pour BaobabGeekInterpreterException."""

    def test_init_with_message_only(self) -> None:
        """Test l'initialisation avec uniquement un message."""
        message = "Test error message"
        exception = BaobabGeekInterpreterException(message)

        assert exception.message == message
        assert exception.source is None
        assert exception.position is None
        assert exception.line is None
        assert exception.column is None

    def test_init_with_all_parameters(self) -> None:
        """Test l'initialisation avec tous les paramètres."""
        message = "Test error"
        source = "service(1, 2)"
        position = 7
        line = 1
        column = 8

        exception = BaobabGeekInterpreterException(
            message=message, source=source, position=position, line=line, column=column
        )

        assert exception.message == message
        assert exception.source == source
        assert exception.position == position
        assert exception.line == line
        assert exception.column == column

    def test_init_with_partial_parameters(self) -> None:
        """Test l'initialisation avec des paramètres partiels."""
        message = "Test error"
        line = 5

        exception = BaobabGeekInterpreterException(message=message, line=line)

        assert exception.message == message
        assert exception.source is None
        assert exception.position is None
        assert exception.line == line
        assert exception.column is None

    def test_str_with_line_and_column(self) -> None:
        """Test la représentation en chaîne avec ligne et colonne."""
        exception = BaobabGeekInterpreterException("Syntax error", line=10, column=15)

        result = str(exception)

        assert result == "Syntax error at line 10, column 15"

    def test_str_with_line_only(self) -> None:
        """Test la représentation en chaîne avec uniquement la ligne."""
        exception = BaobabGeekInterpreterException("Syntax error", line=10)

        result = str(exception)

        assert result == "Syntax error"

    def test_str_with_column_only(self) -> None:
        """Test la représentation en chaîne avec uniquement la colonne."""
        exception = BaobabGeekInterpreterException("Syntax error", column=15)

        result = str(exception)

        assert result == "Syntax error"

    def test_str_without_line_and_column(self) -> None:
        """Test la représentation en chaîne sans ligne ni colonne."""
        exception = BaobabGeekInterpreterException("Simple error")

        result = str(exception)

        assert result == "Simple error"

    def test_inherits_from_exception(self) -> None:
        """Test que la classe hérite bien de Exception."""
        exception = BaobabGeekInterpreterException("Test")

        assert isinstance(exception, Exception)

    def test_can_be_raised_and_caught(self) -> None:
        """Test que l'exception peut être levée et attrapée."""
        with pytest.raises(BaobabGeekInterpreterException) as exc_info:
            raise BaobabGeekInterpreterException("Test exception")

        assert exc_info.value.message == "Test exception"

    def test_can_be_caught_as_exception(self) -> None:
        """Test que l'exception peut être attrapée comme Exception."""
        try:
            raise BaobabGeekInterpreterException("Test")
        except Exception as e:
            assert isinstance(e, BaobabGeekInterpreterException)
            assert str(e) == "Test"

    def test_message_attribute_is_accessible(self) -> None:
        """Test que l'attribut message est accessible."""
        exception = BaobabGeekInterpreterException("Test message")

        assert hasattr(exception, "message")
        assert exception.message == "Test message"

    def test_all_attributes_are_accessible(self) -> None:
        """Test que tous les attributs sont accessibles."""
        exception = BaobabGeekInterpreterException(
            message="Test",
            source="code",
            position=5,
            line=2,
            column=3,
        )

        assert hasattr(exception, "message")
        assert hasattr(exception, "source")
        assert hasattr(exception, "position")
        assert hasattr(exception, "line")
        assert hasattr(exception, "column")

    def test_with_multiline_source(self) -> None:
        """Test avec un code source multi-ligne."""
        source = "service(1, 2)\nservice(3, 4)"
        exception = BaobabGeekInterpreterException(
            "Error in second line", source=source, line=2, column=1
        )

        assert exception.source == source
        assert str(exception) == "Error in second line at line 2, column 1"

    def test_with_zero_position(self) -> None:
        """Test avec une position à zéro."""
        exception = BaobabGeekInterpreterException("Error at start", position=0, line=1, column=1)

        assert exception.position == 0
        assert exception.line == 1
        assert exception.column == 1

    def test_with_large_position_values(self) -> None:
        """Test avec des valeurs de position importantes."""
        exception = BaobabGeekInterpreterException(
            "Error far in file", position=10000, line=500, column=80
        )

        assert exception.position == 10000
        assert exception.line == 500
        assert exception.column == 80
        assert "line 500, column 80" in str(exception)
