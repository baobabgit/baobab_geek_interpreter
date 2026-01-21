"""Tests d'intégration pour SemanticAnalyzer avec lexer et parser."""

import pytest

from baobab_geek_interpreter.exceptions.semantic_exception import (
    BaobabSemanticAnalyserException,
)
from baobab_geek_interpreter.execution.service_decorator import service
from baobab_geek_interpreter.lexical.lexical_analyzer import LexicalAnalyzer
from baobab_geek_interpreter.semantic.semantic_analyzer import SemanticAnalyzer
from baobab_geek_interpreter.semantic.symbol_table import SymbolTable
from baobab_geek_interpreter.syntax.syntax_analyzer import SyntaxAnalyzer


class TestSemanticAnalyzerIntegrationValidCases:
    """Tests d'intégration pour les cas valides."""

    def test_full_pipeline_simple_service(self) -> None:
        """Test du pipeline complet pour un service simple."""
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
        analyzer.analyze(ast)  # Ne doit pas lever d'exception

    def test_full_pipeline_with_array(self) -> None:
        """Test du pipeline avec un tableau."""
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

    def test_full_pipeline_mixed_types(self) -> None:
        """Test du pipeline avec types mixtes."""
        table = SymbolTable()

        @service
        def process(x: int, y: float, z: str) -> None:
            pass

        table.register("process", process)

        source = 'process(42, 3.14, "hello")'
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

    def test_full_pipeline_empty_array(self) -> None:
        """Test du pipeline avec tableau vide."""
        table = SymbolTable()

        @service
        def process_empty(items: list[int]) -> None:
            pass

        table.register("process_empty", process_empty)

        source = "process_empty([])"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)


class TestSemanticAnalyzerIntegrationErrors:
    """Tests d'intégration pour les cas d'erreur."""

    def test_full_pipeline_unknown_service(self) -> None:
        """Test avec service inconnu."""
        table = SymbolTable()

        source = "unknown_service(42)"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        with pytest.raises(BaobabSemanticAnalyserException, match="Service inconnu"):
            analyzer.analyze(ast)

    def test_full_pipeline_type_mismatch(self) -> None:
        """Test avec types incompatibles."""
        table = SymbolTable()

        @service
        def add(a: int, b: int) -> int:
            return a + b

        table.register("add", add)

        source = 'add(10, "20")'
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        with pytest.raises(
            BaobabSemanticAnalyserException, match="Types d'arguments incompatibles"
        ):
            analyzer.analyze(ast)

    def test_full_pipeline_wrong_number_of_args(self) -> None:
        """Test avec mauvais nombre d'arguments."""
        table = SymbolTable()

        @service
        def add(a: int, b: int) -> int:
            return a + b

        table.register("add", add)

        source = "add(10)"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        with pytest.raises(
            BaobabSemanticAnalyserException, match="Types d'arguments incompatibles"
        ):
            analyzer.analyze(ast)

    def test_full_pipeline_heterogeneous_array(self) -> None:
        """Test avec tableau hétérogène."""
        table = SymbolTable()

        @service
        def process(numbers: list[int]) -> None:
            pass

        table.register("process", process)

        source = "process([1, 2.5, 3])"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        with pytest.raises(
            BaobabSemanticAnalyserException, match="tableaux doivent être homogènes"
        ):
            analyzer.analyze(ast)

    def test_full_pipeline_nested_arrays(self) -> None:
        """Test avec tableaux imbriqués."""
        table = SymbolTable()

        @service
        def process(data: list[list[int]]) -> None:
            pass

        table.register("process", process)

        source = "process([[1, 2], [3, 4]])"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        with pytest.raises(BaobabSemanticAnalyserException, match="tableaux imbriqués"):
            analyzer.analyze(ast)


class TestSemanticAnalyzerIntegrationComplexCases:
    """Tests d'intégration pour des cas complexes."""

    def test_full_pipeline_multiple_arrays(self) -> None:
        """Test avec plusieurs tableaux."""
        table = SymbolTable()

        @service
        def merge(a: list[int], b: list[int]) -> list[int]:
            return a + b

        table.register("merge", merge)

        source = "merge([1, 2], [3, 4])"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

    def test_full_pipeline_string_array(self) -> None:
        """Test avec tableau de chaînes."""
        table = SymbolTable()

        @service
        def join_strings(words: list[str]) -> str:
            return " ".join(words)

        table.register("join_strings", join_strings)

        source = 'join_strings(["hello", "world"])'
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

    def test_full_pipeline_float_array(self) -> None:
        """Test avec tableau de flottants."""
        table = SymbolTable()

        @service
        def average(numbers: list[float]) -> float:
            return sum(numbers) / len(numbers) if numbers else 0.0

        table.register("average", average)

        source = "average([1.5, 2.5, 3.5])"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

    def test_full_pipeline_complex_signature(self) -> None:
        """Test avec signature complexe."""
        table = SymbolTable()

        @service
        def complex_func(a: int, b: float, c: str, d: list[int], e: list[str]) -> None:
            pass

        table.register("complex_func", complex_func)

        source = 'complex_func(42, 3.14, "test", [1, 2, 3], ["a", "b"])'
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

    def test_full_pipeline_negative_numbers(self) -> None:
        """Test avec nombres négatifs."""
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


class TestSemanticAnalyzerIntegrationEdgeCases:
    """Tests d'intégration pour les cas limites."""

    def test_full_pipeline_service_without_annotations(self) -> None:
        """Test avec service sans annotations de type."""
        table = SymbolTable()

        @service
        def no_types(a, b):  # type: ignore
            return a + b

        table.register("no_types", no_types)

        source = 'no_types(1, "hello")'
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)  # Accepte tout sans annotations

    def test_full_pipeline_single_array_element(self) -> None:
        """Test avec tableau à un seul élément."""
        table = SymbolTable()

        @service
        def process(numbers: list[int]) -> None:
            pass

        table.register("process", process)

        source = "process([42])"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)

    def test_full_pipeline_large_array(self) -> None:
        """Test avec grand tableau."""
        table = SymbolTable()

        @service
        def process(numbers: list[int]) -> None:
            pass

        table.register("process", process)

        source = "process([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])"
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        analyzer = SemanticAnalyzer(table)
        analyzer.analyze(ast)
