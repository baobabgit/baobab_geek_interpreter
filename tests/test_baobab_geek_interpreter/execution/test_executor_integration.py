"""Tests d'intégration pour Executor avec le pipeline complet."""

import pytest

from baobab_geek_interpreter.exceptions.execution_exception import (
    BaobabExecutionException,
)
from baobab_geek_interpreter.execution.executor import Executor
from baobab_geek_interpreter.execution.service_decorator import service
from baobab_geek_interpreter.lexical.lexical_analyzer import LexicalAnalyzer
from baobab_geek_interpreter.semantic.semantic_analyzer import SemanticAnalyzer
from baobab_geek_interpreter.semantic.symbol_table import SymbolTable
from baobab_geek_interpreter.syntax.syntax_analyzer import SyntaxAnalyzer


class TestExecutorIntegrationBasic:
    """Tests d'intégration basiques."""

    def test_full_pipeline_simple_addition(self) -> None:
        """Test du pipeline complet pour une addition simple."""
        # Préparer la table des symboles
        table = SymbolTable()

        @service
        def add(a: int, b: int) -> int:
            return a + b

        table.register("add", add)

        # Pipeline complet
        source = "add(10, 20)"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        result = executor.execute(ast)

        assert result == 30

    def test_full_pipeline_string_concat(self) -> None:
        """Test du pipeline complet pour une concaténation."""
        table = SymbolTable()

        @service
        def concat(a: str, b: str) -> str:
            return a + b

        table.register("concat", concat)

        source = 'concat("Hello", " World")'
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        result = executor.execute(ast)

        assert result == "Hello World"

    def test_full_pipeline_float_multiplication(self) -> None:
        """Test du pipeline complet pour une multiplication."""
        table = SymbolTable()

        @service
        def multiply(a: float, b: float) -> float:
            return a * b

        table.register("multiply", multiply)

        source = "multiply(2.5, 4.0)"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        result = executor.execute(ast)

        assert result == 10.0


class TestExecutorIntegrationArrays:
    """Tests d'intégration avec des tableaux."""

    def test_full_pipeline_sum_array(self) -> None:
        """Test du pipeline complet avec somme de tableau."""
        table = SymbolTable()

        @service
        def sum_numbers(numbers: list[int]) -> int:
            return sum(numbers)

        table.register("sum_numbers", sum_numbers)

        source = "sum_numbers([1, 2, 3, 4, 5])"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        result = executor.execute(ast)

        assert result == 15

    def test_full_pipeline_join_strings(self) -> None:
        """Test du pipeline complet avec jointure de chaînes."""
        table = SymbolTable()

        @service
        def join_words(words: list[str]) -> str:
            return " ".join(words)

        table.register("join_words", join_words)

        source = 'join_words(["Hello", "beautiful", "world"])'
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        result = executor.execute(ast)

        assert result == "Hello beautiful world"

    def test_full_pipeline_average_floats(self) -> None:
        """Test du pipeline complet avec moyenne de flottants."""
        table = SymbolTable()

        @service
        def average(numbers: list[float]) -> float:
            return sum(numbers) / len(numbers) if numbers else 0.0

        table.register("average", average)

        source = "average([1.5, 2.5, 3.5, 4.5])"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        result = executor.execute(ast)

        assert result == 3.0

    def test_full_pipeline_empty_array(self) -> None:
        """Test du pipeline complet avec tableau vide."""
        table = SymbolTable()

        @service
        def count_items(items: list[int]) -> int:
            return len(items)

        table.register("count_items", count_items)

        source = "count_items([])"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        result = executor.execute(ast)

        assert result == 0


class TestExecutorIntegrationMixedTypes:
    """Tests d'intégration avec types mixtes."""

    def test_full_pipeline_mixed_arguments(self) -> None:
        """Test du pipeline complet avec arguments mixtes."""
        table = SymbolTable()

        @service
        def format_price(quantity: int, price: float, name: str) -> str:
            total = quantity * price
            return f"{quantity} x {name} = ${total:.2f}"

        table.register("format_price", format_price)

        source = 'format_price(3, 9.99, "apple")'
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        result = executor.execute(ast)

        assert result == "3 x apple = $29.97"

    def test_full_pipeline_array_and_scalar(self) -> None:
        """Test du pipeline complet avec tableau et scalaire."""
        table = SymbolTable()

        @service
        def multiply_all(numbers: list[int], factor: int) -> list[int]:
            return [n * factor for n in numbers]

        table.register("multiply_all", multiply_all)

        source = "multiply_all([1, 2, 3], 5)"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        result = executor.execute(ast)

        assert result == [5, 10, 15]


class TestExecutorIntegrationExceptions:
    """Tests d'intégration pour la gestion des exceptions."""

    def test_full_pipeline_division_by_zero(self) -> None:
        """Test du pipeline complet avec division par zéro."""
        table = SymbolTable()

        @service
        def divide(a: int, b: int) -> float:
            return a / b

        table.register("divide", divide)

        source = "divide(10, 0)"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        with pytest.raises(BaobabExecutionException) as exc_info:
            executor.execute(ast)

        assert "divide" in str(exc_info.value)
        assert exc_info.value.service_name == "divide"
        assert isinstance(exc_info.value.original_exception, ZeroDivisionError)

    def test_full_pipeline_custom_exception(self) -> None:
        """Test du pipeline complet avec exception personnalisée."""
        table = SymbolTable()

        @service
        def validate_positive(value: int) -> str:
            if value <= 0:
                raise ValueError("Value must be positive")
            return "Valid"

        table.register("validate_positive", validate_positive)

        source = "validate_positive(-5)"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        with pytest.raises(BaobabExecutionException) as exc_info:
            executor.execute(ast)

        assert "validate_positive" in str(exc_info.value)
        assert isinstance(exc_info.value.original_exception, ValueError)
        assert "positive" in str(exc_info.value.original_exception)


class TestExecutorIntegrationComplexScenarios:
    """Tests d'intégration pour des scénarios complexes."""

    def test_full_pipeline_negative_numbers(self) -> None:
        """Test du pipeline complet avec nombres négatifs."""
        table = SymbolTable()

        @service
        def subtract(a: int, b: int) -> int:
            return a - b

        table.register("subtract", subtract)

        source = "subtract(-10, -5)"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        result = executor.execute(ast)

        assert result == -5

    def test_full_pipeline_large_array(self) -> None:
        """Test du pipeline complet avec grand tableau."""
        table = SymbolTable()

        @service
        def max_value(numbers: list[int]) -> int:
            return max(numbers) if numbers else 0

        table.register("max_value", max_value)

        source = "max_value([5, 2, 9, 1, 7, 3, 8, 4, 6])"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        result = executor.execute(ast)

        assert result == 9

    def test_full_pipeline_service_returns_list(self) -> None:
        """Test du pipeline complet avec service retournant une liste."""
        table = SymbolTable()

        @service
        def create_range(start: int, end: int) -> list[int]:
            return list(range(start, end))

        table.register("create_range", create_range)

        source = "create_range(1, 6)"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        result = executor.execute(ast)

        assert result == [1, 2, 3, 4, 5]

    def test_full_pipeline_service_no_return(self) -> None:
        """Test du pipeline complet avec service sans retour."""
        table = SymbolTable()

        # Variable pour vérifier l'exécution
        executed = []

        @service
        def log_message(message: str) -> None:
            executed.append(message)

        table.register("log_message", log_message)

        source = 'log_message("Test message")'
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        result = executor.execute(ast)

        assert result is None
        assert executed == ["Test message"]


class TestExecutorIntegrationRealWorld:
    """Tests d'intégration pour des cas d'usage réels."""

    def test_full_pipeline_calculate_total(self) -> None:
        """Test du pipeline complet pour un calcul de total."""
        table = SymbolTable()

        @service
        def calculate_total(prices: list[float], tax_rate: float) -> float:
            subtotal = sum(prices)
            return subtotal * (1 + tax_rate)

        table.register("calculate_total", calculate_total)

        source = "calculate_total([10.0, 20.0, 30.0], 0.2)"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        result = executor.execute(ast)

        assert result == 72.0  # (10 + 20 + 30) * 1.2

    def test_full_pipeline_filter_by_length(self) -> None:
        """Test du pipeline complet pour filtrage par longueur."""
        table = SymbolTable()

        @service
        def filter_long_words(words: list[str], min_length: int) -> list[str]:
            return [w for w in words if len(w) >= min_length]

        table.register("filter_long_words", filter_long_words)

        source = 'filter_long_words(["hi", "hello", "hey", "world"], 5)'
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        result = executor.execute(ast)

        assert result == ["hello", "world"]

    def test_full_pipeline_format_report(self) -> None:
        """Test du pipeline complet pour formatage de rapport."""
        table = SymbolTable()

        @service
        def format_report(title: str, count: int, values: list[float]) -> str:
            avg = sum(values) / len(values) if values else 0
            return f"{title}: {count} items, average = {avg:.2f}"

        table.register("format_report", format_report)

        source = 'format_report("Sales", 3, [100.0, 200.0, 300.0])'
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

        executor = Executor(table)
        result = executor.execute(ast)

        assert result == "Sales: 3 items, average = 200.00"
