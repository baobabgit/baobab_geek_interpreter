"""Tests unitaires pour la classe SyntaxAnalyzer."""

import pytest

from baobab_geek_interpreter.exceptions.syntax_exception import (
    BaobabSyntaxAnalyserException,
)
from baobab_geek_interpreter.lexical.lexical_analyzer import LexicalAnalyzer
from baobab_geek_interpreter.syntax.ast_node import (
    ArrayNode,
    FloatNode,
    IntNode,
    ServiceCallNode,
    StringNode,
)
from baobab_geek_interpreter.syntax.syntax_analyzer import SyntaxAnalyzer


class TestSyntaxAnalyzerBasics:
    """Tests de base pour SyntaxAnalyzer."""

    def test_analyzer_creation(self) -> None:
        """Test la création d'un analyseur syntaxique."""
        analyzer = SyntaxAnalyzer()
        assert analyzer is not None

    def test_parse_empty_token_list_raises_error(self) -> None:
        """Test que parser une liste vide lève une exception."""
        analyzer = SyntaxAnalyzer()

        with pytest.raises(BaobabSyntaxAnalyserException, match="vide"):
            analyzer.parse([])


class TestSyntaxAnalyzerSimpleServiceCalls:
    """Tests pour les appels de service simples."""

    def test_parse_service_call_no_args(self) -> None:
        """Test un appel de service sans arguments."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze("myService()")

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert isinstance(ast, ServiceCallNode)
        assert ast.name == "myService"
        assert len(ast.arguments) == 0

    def test_parse_service_call_with_int_arg(self) -> None:
        """Test un appel de service avec un argument entier."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze("calculate(42)")

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert isinstance(ast, ServiceCallNode)
        assert ast.name == "calculate"
        assert len(ast.arguments) == 1
        assert isinstance(ast.arguments[0].value, IntNode)
        assert ast.arguments[0].value.value == 42

    def test_parse_service_call_with_negative_int(self) -> None:
        """Test un appel de service avec un entier négatif."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze("subtract(-5)")

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert ast.arguments[0].value.value == -5

    def test_parse_service_call_with_float_arg(self) -> None:
        """Test un appel de service avec un argument flottant."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze("calculatePi(3.14)")

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert isinstance(ast.arguments[0].value, FloatNode)
        assert ast.arguments[0].value.value == 3.14

    def test_parse_service_call_with_string_arg(self) -> None:
        """Test un appel de service avec un argument chaîne."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze('greet("hello")')

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert isinstance(ast.arguments[0].value, StringNode)
        assert ast.arguments[0].value.value == "hello"

    def test_parse_service_call_with_empty_string(self) -> None:
        """Test un appel de service avec une chaîne vide."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze('test("")')

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert ast.arguments[0].value.value == ""


class TestSyntaxAnalyzerMultipleArguments:
    """Tests pour les appels avec plusieurs arguments."""

    def test_parse_service_call_with_two_args(self) -> None:
        """Test un appel de service avec deux arguments."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze("add(10, 20)")

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert len(ast.arguments) == 2
        assert ast.arguments[0].value.value == 10
        assert ast.arguments[1].value.value == 20

    def test_parse_service_call_with_three_args(self) -> None:
        """Test un appel de service avec trois arguments."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze('process(1, 2.5, "test")')

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert len(ast.arguments) == 3
        assert isinstance(ast.arguments[0].value, IntNode)
        assert isinstance(ast.arguments[1].value, FloatNode)
        assert isinstance(ast.arguments[2].value, StringNode)

    def test_parse_service_call_with_mixed_types(self) -> None:
        """Test un appel avec différents types d'arguments."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze('mixed(42, -3.14, "hello", 0)')

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert len(ast.arguments) == 4
        assert ast.arguments[0].value.value == 42
        assert ast.arguments[1].value.value == -3.14
        assert ast.arguments[2].value.value == "hello"
        assert ast.arguments[3].value.value == 0


class TestSyntaxAnalyzerArrays:
    """Tests pour les tableaux."""

    def test_parse_empty_array(self) -> None:
        """Test un tableau vide."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze("test([])")

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert len(ast.arguments) == 1
        assert isinstance(ast.arguments[0].value, ArrayNode)
        assert len(ast.arguments[0].value.elements) == 0

    def test_parse_array_of_integers(self) -> None:
        """Test un tableau d'entiers."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze("process([1, 2, 3])")

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        array = ast.arguments[0].value
        assert isinstance(array, ArrayNode)
        assert len(array.elements) == 3
        assert array.elements[0].value == 1
        assert array.elements[1].value == 2
        assert array.elements[2].value == 3

    def test_parse_array_of_floats(self) -> None:
        """Test un tableau de flottants."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze("calculate([1.5, 2.5, 3.5])")

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        array = ast.arguments[0].value
        assert len(array.elements) == 3
        assert all(isinstance(elem, FloatNode) for elem in array.elements)

    def test_parse_array_of_strings(self) -> None:
        """Test un tableau de chaînes."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze('names(["Alice", "Bob", "Charlie"])')

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        array = ast.arguments[0].value
        assert len(array.elements) == 3
        assert array.elements[0].value == "Alice"
        assert array.elements[1].value == "Bob"
        assert array.elements[2].value == "Charlie"

    def test_parse_multiple_arrays(self) -> None:
        """Test plusieurs tableaux comme arguments."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze("merge([1, 2], [3, 4])")

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert len(ast.arguments) == 2
        assert isinstance(ast.arguments[0].value, ArrayNode)
        assert isinstance(ast.arguments[1].value, ArrayNode)


class TestSyntaxAnalyzerErrors:
    """Tests pour la gestion des erreurs."""

    def test_missing_opening_parenthesis_raises_error(self) -> None:
        """Test qu'une parenthèse ouvrante manquante lève une exception."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze("service)")

        parser = SyntaxAnalyzer()

        with pytest.raises(BaobabSyntaxAnalyserException, match="attendu LPAREN"):
            parser.parse(tokens)

    def test_missing_closing_parenthesis_raises_error(self) -> None:
        """Test qu'une parenthèse fermante manquante lève une exception."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze("service(")

        parser = SyntaxAnalyzer()

        with pytest.raises(BaobabSyntaxAnalyserException):
            parser.parse(tokens)

    def test_missing_closing_bracket_raises_error(self) -> None:
        """Test qu'un crochet fermant manquant lève une exception."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze("service([1, 2")

        parser = SyntaxAnalyzer()

        with pytest.raises(BaobabSyntaxAnalyserException):
            parser.parse(tokens)

    def test_unexpected_token_after_service_call_raises_error(self) -> None:
        """Test qu'un token inattendu après l'appel lève une exception."""
        lexer = LexicalAnalyzer()
        # Ajouter manuellement un token supplémentaire après l'appel
        tokens = lexer.analyze("service()")
        # Insérer un token avant EOF
        tokens.insert(-1, tokens[0])  # Dupliquer le premier token

        parser = SyntaxAnalyzer()

        with pytest.raises(BaobabSyntaxAnalyserException, match="Contenu inattendu"):
            parser.parse(tokens)

    def test_missing_comma_between_arguments_raises_error(self) -> None:
        """Test qu'une virgule manquante entre arguments lève une exception."""
        lexer = LexicalAnalyzer()
        # Créer manuellement des tokens sans virgule
        tokens = lexer.analyze("service(1, 2)")
        # Retirer la virgule (token à l'index 3)
        tokens.pop(3)

        parser = SyntaxAnalyzer()

        with pytest.raises(BaobabSyntaxAnalyserException):
            parser.parse(tokens)

    def test_invalid_constant_type_raises_error(self) -> None:
        """Test qu'un type de constante invalide lève une exception."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze("service(42)")
        # Remplacer le token INT par un token invalide (LPAREN)
        tokens[2] = tokens[1]  # Remplacer 42 par (

        parser = SyntaxAnalyzer()

        with pytest.raises(BaobabSyntaxAnalyserException, match="Constante attendue"):
            parser.parse(tokens)


class TestSyntaxAnalyzerComplexScenarios:
    """Tests pour des scénarios complexes."""

    def test_parse_service_with_array_and_scalars(self) -> None:
        """Test un service avec tableaux et scalaires mélangés."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze('complex(42, [1, 2, 3], "test", 3.14)')

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert len(ast.arguments) == 4
        assert isinstance(ast.arguments[0].value, IntNode)
        assert isinstance(ast.arguments[1].value, ArrayNode)
        assert isinstance(ast.arguments[2].value, StringNode)
        assert isinstance(ast.arguments[3].value, FloatNode)

    def test_parse_service_with_nested_arrays_structure(self) -> None:
        """Test la structure d'un service avec tableaux imbriqués."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze("nested([[1, 2], [3, 4]])")

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        # Vérifier la structure (validation sémantique sera faite plus tard)
        outer_array = ast.arguments[0].value
        assert isinstance(outer_array, ArrayNode)
        assert len(outer_array.elements) == 2
        assert isinstance(outer_array.elements[0], ArrayNode)
        assert isinstance(outer_array.elements[1], ArrayNode)

    def test_parse_service_with_single_element_array(self) -> None:
        """Test un tableau avec un seul élément."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze("single([42])")

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        array = ast.arguments[0].value
        assert len(array.elements) == 1
        assert array.elements[0].value == 42

    def test_parse_service_with_string_containing_special_chars(self) -> None:
        """Test une chaîne avec caractères spéciaux échappés."""
        lexer = LexicalAnalyzer()
        tokens = lexer.analyze(r'test("hello\nworld")')

        parser = SyntaxAnalyzer()
        ast = parser.parse(tokens)

        assert "hello\nworld" in ast.arguments[0].value.value
