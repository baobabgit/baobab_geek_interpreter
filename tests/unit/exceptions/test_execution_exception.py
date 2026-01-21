"""Tests unitaires pour la classe BaobabExecutionException."""

import pytest

from baobab_geek_interpreter.exceptions.base_exception import (
    BaobabGeekInterpreterException,
)
from baobab_geek_interpreter.exceptions.execution_exception import (
    BaobabExecutionException,
)


class TestBaobabExecutionException:
    """Classe de tests pour BaobabExecutionException."""

    def test_inherits_from_base_exception(self) -> None:
        """Test que la classe hérite de BaobabGeekInterpreterException."""
        exception = BaobabExecutionException("Test error", service_name="test_service")

        assert isinstance(exception, BaobabGeekInterpreterException)
        assert isinstance(exception, Exception)

    def test_init_with_required_parameters(self) -> None:
        """Test l'initialisation avec les paramètres requis."""
        message = "Execution error"
        service_name = "my_service"

        exception = BaobabExecutionException(message=message, service_name=service_name)

        assert exception.message == message
        assert exception.service_name == service_name
        assert exception.original_exception is None
        assert exception.source is None
        assert exception.position is None
        assert exception.line is None
        assert exception.column is None

    def test_init_with_all_parameters(self) -> None:
        """Test l'initialisation avec tous les paramètres."""
        message = "Division by zero"
        service_name = "divide"
        original_exception = ZeroDivisionError("division by zero")
        source = "divide(10, 0)"
        position = 0
        line = 1
        column = 1

        exception = BaobabExecutionException(
            message=message,
            service_name=service_name,
            original_exception=original_exception,
            source=source,
            position=position,
            line=line,
            column=column,
        )

        assert exception.message == message
        assert exception.service_name == service_name
        assert exception.original_exception is original_exception
        assert exception.source == source
        assert exception.position == position
        assert exception.line == line
        assert exception.column == column

    def test_str_with_service_only(self) -> None:
        """Test la représentation en chaîne avec uniquement le service."""
        exception = BaobabExecutionException("Error occurred", service_name="test_svc")

        result = str(exception)

        assert result == "Error occurred in service 'test_svc'"

    def test_str_with_service_and_line_column(self) -> None:
        """Test la représentation en chaîne avec service, ligne et colonne."""
        exception = BaobabExecutionException(
            "Error occurred", service_name="test_svc", line=5, column=10
        )

        result = str(exception)

        assert result == "Error occurred at line 5, column 10 in service 'test_svc'"

    def test_str_with_original_exception(self) -> None:
        """Test la représentation en chaîne avec exception d'origine."""
        original = ValueError("invalid value")
        exception = BaobabExecutionException(
            "Error in service", service_name="validate", original_exception=original
        )

        result = str(exception)

        assert result == "Error in service in service 'validate': invalid value"

    def test_str_with_all_info(self) -> None:
        """Test la représentation en chaîne avec toutes les informations."""
        original = ZeroDivisionError("division by zero")
        exception = BaobabExecutionException(
            "Division error",
            service_name="divide",
            original_exception=original,
            line=3,
            column=5,
        )

        result = str(exception)

        assert (
            result
            == "Division error at line 3, column 5 in service 'divide': division by zero"
        )

    def test_can_be_raised_and_caught(self) -> None:
        """Test que l'exception peut être levée et attrapée."""
        with pytest.raises(BaobabExecutionException) as exc_info:
            raise BaobabExecutionException("Execution error", service_name="test")

        assert exc_info.value.message == "Execution error"
        assert exc_info.value.service_name == "test"

    def test_can_be_caught_as_base_exception(self) -> None:
        """Test que l'exception peut être attrapée comme BaobabGeekInterpreterException."""
        try:
            raise BaobabExecutionException("Test", service_name="svc")
        except BaobabGeekInterpreterException as e:
            assert isinstance(e, BaobabExecutionException)
            assert "svc" in str(e)

    def test_wrapping_real_exception(self) -> None:
        """Test l'encapsulation d'une vraie exception."""
        try:
            result = 10 / 0
        except ZeroDivisionError as e:
            wrapped = BaobabExecutionException(
                "Division failed", service_name="calculator", original_exception=e
            )

            assert wrapped.original_exception is e
            assert isinstance(wrapped.original_exception, ZeroDivisionError)
            assert "division by zero" in str(wrapped)

    def test_service_name_is_accessible(self) -> None:
        """Test que l'attribut service_name est accessible."""
        exception = BaobabExecutionException("Error", service_name="my_service")

        assert hasattr(exception, "service_name")
        assert exception.service_name == "my_service"

    def test_original_exception_is_accessible(self) -> None:
        """Test que l'attribut original_exception est accessible."""
        original = RuntimeError("test")
        exception = BaobabExecutionException(
            "Error", service_name="svc", original_exception=original
        )

        assert hasattr(exception, "original_exception")
        assert exception.original_exception is original
