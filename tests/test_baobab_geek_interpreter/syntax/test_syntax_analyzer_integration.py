"""Tests d'intégration pour la classe SyntaxAnalyzer."""

import pytest

from baobab_geek_interpreter.lexical.lexical_analyzer import LexicalAnalyzer
from baobab_geek_interpreter.syntax.ast_node import (
    ArrayNode,
    FloatNode,
    IntNode,
    ServiceCallNode,
    StringNode,
)
from baobab_geek_interpreter.syntax.syntax_analyzer import SyntaxAnalyzer


class TestSyntaxAnalyzerIntegrationRealWorld:
    """Tests d'intégration avec des scénarios réalistes."""

    def test_full_pipeline_simple_service(self) -> None:
        """Test le pipeline complet lexer + parser pour un service simple."""
        source = "calculateSum(10, 20, 30)"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert ast.name == "calculateSum"
        assert len(ast.arguments) == 3
        assert all(isinstance(arg.value, IntNode) for arg in ast.arguments)

    def test_full_pipeline_with_array(self) -> None:
        """Test le pipeline complet avec un tableau."""
        source = "processNumbers([1, 2, 3, 4, 5])"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert ast.name == "processNumbers"
        array = ast.arguments[0].value
        assert isinstance(array, ArrayNode)
        assert len(array.elements) == 5

    def test_full_pipeline_mixed_arguments(self) -> None:
        """Test le pipeline complet avec arguments mixtes."""
        source = 'complexOperation(42, 3.14, "result", [1, 2, 3])'

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert len(ast.arguments) == 4
        assert isinstance(ast.arguments[0].value, IntNode)
        assert isinstance(ast.arguments[1].value, FloatNode)
        assert isinstance(ast.arguments[2].value, StringNode)
        assert isinstance(ast.arguments[3].value, ArrayNode)

    def test_full_pipeline_negative_numbers(self) -> None:
        """Test le pipeline complet avec nombres négatifs."""
        source = "calculate(-10, -3.14, [-1, -2, -3])"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert ast.arguments[0].value.value == -10
        assert ast.arguments[1].value.value == -3.14
        array = ast.arguments[2].value
        assert all(elem.value < 0 for elem in array.elements)

    def test_full_pipeline_empty_service(self) -> None:
        """Test le pipeline complet pour un service sans arguments."""
        source = "initialize()"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert ast.name == "initialize"
        assert len(ast.arguments) == 0


class TestSyntaxAnalyzerIntegrationStringHandling:
    """Tests d'intégration pour la gestion des chaînes."""

    def test_string_with_spaces(self) -> None:
        """Test une chaîne avec espaces."""
        source = 'greet("Hello World")'

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert ast.arguments[0].value.value == "Hello World"

    def test_string_with_escaped_quotes(self) -> None:
        """Test une chaîne avec guillemets échappés."""
        source = r'print("She said \"Hello\"")'

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert '"' in ast.arguments[0].value.value

    def test_string_with_newline(self) -> None:
        """Test une chaîne avec newline échappé."""
        source = r'multiline("line1\nline2")'

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert "\n" in ast.arguments[0].value.value

    def test_empty_string_argument(self) -> None:
        """Test une chaîne vide comme argument."""
        source = 'test("")'

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert ast.arguments[0].value.value == ""

    def test_array_of_strings(self) -> None:
        """Test un tableau de chaînes."""
        source = 'names(["Alice", "Bob", "Charlie"])'

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        array = ast.arguments[0].value
        assert len(array.elements) == 3
        assert all(isinstance(elem, StringNode) for elem in array.elements)


class TestSyntaxAnalyzerIntegrationArrays:
    """Tests d'intégration pour les tableaux."""

    def test_empty_array_argument(self) -> None:
        """Test un tableau vide."""
        source = "process([])"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        array = ast.arguments[0].value
        assert isinstance(array, ArrayNode)
        assert len(array.elements) == 0

    def test_single_element_array(self) -> None:
        """Test un tableau avec un seul élément."""
        source = "single([42])"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        array = ast.arguments[0].value
        assert len(array.elements) == 1
        assert array.elements[0].value == 42

    def test_large_array(self) -> None:
        """Test un grand tableau."""
        source = "large([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        array = ast.arguments[0].value
        assert len(array.elements) == 10

    def test_array_of_floats(self) -> None:
        """Test un tableau de flottants."""
        source = "floats([1.1, 2.2, 3.3])"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        array = ast.arguments[0].value
        assert all(isinstance(elem, FloatNode) for elem in array.elements)

    def test_multiple_arrays_as_arguments(self) -> None:
        """Test plusieurs tableaux comme arguments."""
        source = "merge([1, 2], [3, 4], [5, 6])"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert len(ast.arguments) == 3
        assert all(isinstance(arg.value, ArrayNode) for arg in ast.arguments)


class TestSyntaxAnalyzerIntegrationEdgeCases:
    """Tests d'intégration pour les cas limites."""

    def test_service_name_with_underscores(self) -> None:
        """Test un nom de service avec underscores."""
        source = "my_service_name()"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert ast.name == "my_service_name"

    def test_service_name_camel_case(self) -> None:
        """Test un nom de service en CamelCase."""
        source = "MyServiceName()"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert ast.name == "MyServiceName"

    def test_very_large_integer(self) -> None:
        """Test un très grand entier."""
        source = "bigNumber(999999999999)"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert ast.arguments[0].value.value == 999999999999

    def test_float_with_many_decimals(self) -> None:
        """Test un flottant avec beaucoup de décimales."""
        source = "precise(3.141592653589793)"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert ast.arguments[0].value.value == 3.141592653589793

    def test_zero_values(self) -> None:
        """Test des valeurs zéro."""
        source = "zeros(0, 0.0, [0, 0, 0])"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert ast.arguments[0].value.value == 0
        assert ast.arguments[1].value.value == 0.0


class TestSyntaxAnalyzerIntegrationWhitespace:
    """Tests d'intégration pour la gestion des espaces."""

    def test_no_spaces(self) -> None:
        """Test sans espaces."""
        source = "test(1,2,3)"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert len(ast.arguments) == 3

    def test_many_spaces(self) -> None:
        """Test avec beaucoup d'espaces."""
        source = "test  (  1  ,  2  ,  3  )"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert len(ast.arguments) == 3

    def test_tabs_and_newlines(self) -> None:
        """Test avec tabulations et nouvelles lignes."""
        source = "test(\n\t1,\n\t2,\n\t3\n)"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert len(ast.arguments) == 3


class TestSyntaxAnalyzerIntegrationComplexScenarios:
    """Tests d'intégration pour des scénarios complexes."""

    def test_nested_arrays_structure(self) -> None:
        """Test la structure de tableaux imbriqués."""
        source = "nested([[1, 2], [3, 4]])"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        outer_array = ast.arguments[0].value
        assert isinstance(outer_array, ArrayNode)
        assert len(outer_array.elements) == 2
        assert isinstance(outer_array.elements[0], ArrayNode)
        assert isinstance(outer_array.elements[1], ArrayNode)

    def test_all_types_in_one_call(self) -> None:
        """Test tous les types dans un seul appel."""
        source = 'allTypes(42, -3.14, "text", [], [1, 2])'

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert len(ast.arguments) == 5
        assert isinstance(ast.arguments[0].value, IntNode)
        assert isinstance(ast.arguments[1].value, FloatNode)
        assert isinstance(ast.arguments[2].value, StringNode)
        assert isinstance(ast.arguments[3].value, ArrayNode)
        assert isinstance(ast.arguments[4].value, ArrayNode)

    def test_array_with_mixed_number_types(self) -> None:
        """Test un tableau avec entiers et flottants (structure seulement)."""
        source = "mixed([1, 2.5, 3, 4.5])"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        array = ast.arguments[0].value
        assert len(array.elements) == 4
        # La validation sémantique (homogénéité) sera faite plus tard

    def test_long_service_name(self) -> None:
        """Test un nom de service très long."""
        source = "veryLongServiceNameThatIsStillValid()"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert ast.name == "veryLongServiceNameThatIsStillValid"

    def test_many_arguments(self) -> None:
        """Test un appel avec beaucoup d'arguments."""
        source = "many(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)"

        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(source)

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert len(ast.arguments) == 10
