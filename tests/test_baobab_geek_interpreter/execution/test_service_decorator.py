"""Tests unitaires pour le décorateur @service."""

import pytest

from baobab_geek_interpreter.execution.service_decorator import service


class TestServiceDecorator:
    """Tests pour le décorateur @service."""

    def test_decorator_adds_is_service_attribute(self) -> None:
        """Test que le décorateur ajoute l'attribut _is_service."""

        @service
        def my_function() -> str:
            return "result"

        assert hasattr(my_function, "_is_service")
        assert my_function._is_service is True

    def test_decorator_adds_service_name_attribute(self) -> None:
        """Test que le décorateur ajoute l'attribut _service_name."""

        @service
        def calculate() -> int:
            return 42

        assert hasattr(calculate, "_service_name")
        assert calculate._service_name == "calculate"

    def test_decorated_function_executes_correctly(self) -> None:
        """Test que la fonction décorée s'exécute correctement."""

        @service
        def add(a: int, b: int) -> int:
            return a + b

        result = add(3, 5)
        assert result == 8

    def test_decorated_function_with_no_args(self) -> None:
        """Test une fonction sans arguments."""

        @service
        def get_constant() -> int:
            return 42

        assert get_constant() == 42
        assert get_constant._is_service is True

    def test_decorated_function_with_kwargs(self) -> None:
        """Test une fonction avec arguments nommés."""

        @service
        def greet(name: str = "World") -> str:
            return f"Hello, {name}!"

        assert greet() == "Hello, World!"
        assert greet(name="Alice") == "Hello, Alice!"

    def test_decorated_function_preserves_name(self) -> None:
        """Test que le décorateur préserve le nom de la fonction."""

        @service
        def original_name() -> None:
            pass

        assert original_name.__name__ == "original_name"

    def test_decorated_function_preserves_docstring(self) -> None:
        """Test que le décorateur préserve la docstring."""

        @service
        def documented_function() -> None:
            """This is a docstring."""
            pass

        assert documented_function.__doc__ == "This is a docstring."

    def test_multiple_decorated_functions(self) -> None:
        """Test plusieurs fonctions décorées."""

        @service
        def func1() -> int:
            return 1

        @service
        def func2() -> int:
            return 2

        assert func1._is_service is True
        assert func2._is_service is True
        assert func1._service_name == "func1"
        assert func2._service_name == "func2"
        assert func1() == 1
        assert func2() == 2

    def test_decorated_function_with_return_value(self) -> None:
        """Test une fonction avec valeur de retour."""

        @service
        def multiply(x: int, y: int) -> int:
            return x * y

        result = multiply(4, 7)
        assert result == 28

    def test_decorated_function_raises_exception(self) -> None:
        """Test qu'une fonction décorée peut lever des exceptions."""

        @service
        def divide(a: int, b: int) -> float:
            return a / b

        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

    def test_decorated_function_with_complex_return_type(self) -> None:
        """Test une fonction avec type de retour complexe."""

        @service
        def get_list() -> list[int]:
            return [1, 2, 3]

        result = get_list()
        assert result == [1, 2, 3]
        assert isinstance(result, list)

    def test_decorated_function_with_side_effects(self) -> None:
        """Test une fonction avec effets de bord."""
        counter = {"value": 0}

        @service
        def increment() -> int:
            counter["value"] += 1
            return counter["value"]

        assert increment() == 1
        assert increment() == 2
        assert counter["value"] == 2

    def test_decorator_on_lambda_like_function(self) -> None:
        """Test le décorateur sur une fonction lambda-like."""

        @service
        def identity(x: int) -> int:
            return x

        assert identity(42) == 42
        assert identity._is_service is True

    def test_decorated_function_with_varargs(self) -> None:
        """Test une fonction avec *args."""

        @service
        def sum_all(*args: int) -> int:
            return sum(args)

        assert sum_all(1, 2, 3, 4, 5) == 15
        assert sum_all._is_service is True

    def test_decorated_function_with_mixed_args(self) -> None:
        """Test une fonction avec arguments mixtes."""

        @service
        def mixed(a: int, b: int = 10, *args: int, **kwargs: int) -> int:
            return a + b + sum(args) + sum(kwargs.values())

        assert mixed(1) == 11
        assert mixed(1, 2) == 3
        assert mixed(1, 2, 3, 4) == 10
        assert mixed(1, 2, 3, x=10, y=20) == 36
