"""Tests unitaires pour la classe SemanticAnalyzer."""

import pytest

from baobab_geek_interpreter.exceptions.semantic_exception import (
    BaobabSemanticAnalyserException,
)
from baobab_geek_interpreter.execution.service_decorator import service
from baobab_geek_interpreter.semantic.semantic_analyzer import SemanticAnalyzer
from baobab_geek_interpreter.semantic.symbol_table import SymbolTable
from baobab_geek_interpreter.syntax.ast_node import (
    ArgumentNode,
    ArrayNode,
    FloatNode,
    IntNode,
    ServiceCallNode,
    StringNode,
)


class TestSemanticAnalyzerBasics:
    """Tests de base pour SemanticAnalyzer."""

    def test_analyzer_creation(self) -> None:
        """Test la création d'un analyseur sémantique."""
        table = SymbolTable()
        analyzer = SemanticAnalyzer(table)
        assert analyzer is not None

    def test_analyze_unknown_service_raises(self) -> None:
        """Test qu'un service inconnu lève une exception."""
        table = SymbolTable()
        analyzer = SemanticAnalyzer(table)

        ast = ServiceCallNode("unknown", [])

        with pytest.raises(BaobabSemanticAnalyserException, match="Service inconnu"):
            analyzer.analyze(ast)


class TestSemanticAnalyzerValidCases:
    """Tests pour les cas valides."""

    def test_analyze_service_no_args(self) -> None:
        """Test un service sans arguments."""
        table = SymbolTable()

        @service
        def test_service() -> None:
            pass

        table.register("test_service", test_service)
        analyzer = SemanticAnalyzer(table)

        ast = ServiceCallNode("test_service", [])
        analyzer.analyze(ast)  # Ne doit pas lever d'exception

    def test_analyze_service_with_int_args(self) -> None:
        """Test un service avec arguments entiers."""
        table = SymbolTable()

        @service
        def add(a: int, b: int) -> int:
            return a + b

        table.register("add", add)
        analyzer = SemanticAnalyzer(table)

        ast = ServiceCallNode(
            "add",
            [
                ArgumentNode(IntNode(1)),
                ArgumentNode(IntNode(2)),
            ],
        )
        analyzer.analyze(ast)  # Ne doit pas lever d'exception

    def test_analyze_service_with_mixed_types(self) -> None:
        """Test un service avec types mixtes."""
        table = SymbolTable()

        @service
        def process(x: int, y: float, z: str) -> None:
            pass

        table.register("process", process)
        analyzer = SemanticAnalyzer(table)

        ast = ServiceCallNode(
            "process",
            [
                ArgumentNode(IntNode(42)),
                ArgumentNode(FloatNode(3.14)),
                ArgumentNode(StringNode("hello")),
            ],
        )
        analyzer.analyze(ast)

    def test_analyze_service_with_int_array(self) -> None:
        """Test un service avec tableau d'entiers."""
        table = SymbolTable()

        @service
        def process_array(numbers: list[int]) -> None:
            pass

        table.register("process_array", process_array)
        analyzer = SemanticAnalyzer(table)

        ast = ServiceCallNode(
            "process_array",
            [
                ArgumentNode(ArrayNode([IntNode(1), IntNode(2), IntNode(3)])),
            ],
        )
        analyzer.analyze(ast)

    def test_analyze_service_with_empty_array(self) -> None:
        """Test un service avec tableau vide."""
        table = SymbolTable()

        @service
        def process_array(numbers: list[int]) -> None:
            pass

        table.register("process_array", process_array)
        analyzer = SemanticAnalyzer(table)

        ast = ServiceCallNode(
            "process_array",
            [ArgumentNode(ArrayNode([]))],
        )
        analyzer.analyze(ast)


class TestSemanticAnalyzerTypeErrors:
    """Tests pour les erreurs de types."""

    def test_analyze_wrong_argument_type(self) -> None:
        """Test avec type d'argument incorrect."""
        table = SymbolTable()

        @service
        def add(a: int, b: int) -> int:
            return a + b

        table.register("add", add)
        analyzer = SemanticAnalyzer(table)

        # Passer une chaîne au lieu d'un entier
        ast = ServiceCallNode(
            "add",
            [
                ArgumentNode(IntNode(1)),
                ArgumentNode(StringNode("2")),
            ],
        )

        with pytest.raises(
            BaobabSemanticAnalyserException, match="Types d'arguments incompatibles"
        ):
            analyzer.analyze(ast)

    def test_analyze_wrong_number_of_arguments(self) -> None:
        """Test avec mauvais nombre d'arguments."""
        table = SymbolTable()

        @service
        def add(a: int, b: int) -> int:
            return a + b

        table.register("add", add)
        analyzer = SemanticAnalyzer(table)

        # Un seul argument au lieu de deux
        ast = ServiceCallNode("add", [ArgumentNode(IntNode(1))])

        with pytest.raises(
            BaobabSemanticAnalyserException, match="Types d'arguments incompatibles"
        ):
            analyzer.analyze(ast)

    def test_analyze_int_instead_of_float(self) -> None:
        """Test qu'un int n'est pas accepté pour un float."""
        table = SymbolTable()

        @service
        def process(x: float) -> None:
            pass

        table.register("process", process)
        analyzer = SemanticAnalyzer(table)

        # Passer un int au lieu d'un float
        ast = ServiceCallNode("process", [ArgumentNode(IntNode(42))])

        with pytest.raises(
            BaobabSemanticAnalyserException, match="Types d'arguments incompatibles"
        ):
            analyzer.analyze(ast)


class TestSemanticAnalyzerArrayValidation:
    """Tests pour la validation des tableaux."""

    def test_analyze_heterogeneous_array_raises(self) -> None:
        """Test qu'un tableau hétérogène lève une exception."""
        table = SymbolTable()

        @service
        def process(x: list[int]) -> None:
            pass

        table.register("process", process)
        analyzer = SemanticAnalyzer(table)

        # Tableau avec int et float mélangés (hétérogène)
        ast = ServiceCallNode(
            "process",
            [ArgumentNode(ArrayNode([IntNode(1), FloatNode(2.5), IntNode(3)]))],
        )

        with pytest.raises(
            BaobabSemanticAnalyserException, match="tableaux doivent être homogènes"
        ):
            analyzer.analyze(ast)

    def test_analyze_nested_arrays_raises(self) -> None:
        """Test que les tableaux imbriqués lèvent une exception."""
        table = SymbolTable()

        @service
        def process(x: list[list[int]]) -> None:
            pass

        table.register("process", process)
        analyzer = SemanticAnalyzer(table)

        # Tableau avec tableaux imbriqués
        inner1 = ArrayNode([IntNode(1), IntNode(2)])
        inner2 = ArrayNode([IntNode(3), IntNode(4)])
        ast = ServiceCallNode(
            "process",
            [ArgumentNode(ArrayNode([inner1, inner2]))],
        )

        with pytest.raises(BaobabSemanticAnalyserException, match="tableaux imbriqués"):
            analyzer.analyze(ast)

    def test_analyze_array_wrong_element_type(self) -> None:
        """Test avec tableau d'éléments du mauvais type."""
        table = SymbolTable()

        @service
        def process(numbers: list[int]) -> None:
            pass

        table.register("process", process)
        analyzer = SemanticAnalyzer(table)

        # Tableau de strings au lieu d'entiers
        ast = ServiceCallNode(
            "process",
            [ArgumentNode(ArrayNode([StringNode("a"), StringNode("b")]))],
        )

        with pytest.raises(
            BaobabSemanticAnalyserException, match="Types d'arguments incompatibles"
        ):
            analyzer.analyze(ast)


class TestSemanticAnalyzerExtractArguments:
    """Tests pour l'extraction des valeurs d'arguments."""

    def test_extract_simple_values(self) -> None:
        """Test l'extraction de valeurs simples."""
        table = SymbolTable()
        analyzer = SemanticAnalyzer(table)

        ast = ServiceCallNode(
            "test",
            [
                ArgumentNode(IntNode(42)),
                ArgumentNode(FloatNode(3.14)),
                ArgumentNode(StringNode("hello")),
            ],
        )

        values = analyzer._extract_argument_values(ast)
        assert values == [42, 3.14, "hello"]

    def test_extract_array_values(self) -> None:
        """Test l'extraction de tableaux."""
        table = SymbolTable()
        analyzer = SemanticAnalyzer(table)

        ast = ServiceCallNode(
            "test",
            [ArgumentNode(ArrayNode([IntNode(1), IntNode(2), IntNode(3)]))],
        )

        values = analyzer._extract_argument_values(ast)
        assert values == [[1, 2, 3]]

    def test_extract_mixed_values_and_arrays(self) -> None:
        """Test l'extraction de valeurs mixtes et tableaux."""
        table = SymbolTable()
        analyzer = SemanticAnalyzer(table)

        ast = ServiceCallNode(
            "test",
            [
                ArgumentNode(IntNode(42)),
                ArgumentNode(ArrayNode([StringNode("a"), StringNode("b")])),
                ArgumentNode(FloatNode(3.14)),
            ],
        )

        values = analyzer._extract_argument_values(ast)
        assert values == [42, ["a", "b"], 3.14]
