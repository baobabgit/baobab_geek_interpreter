"""Tests d'intégration pour la classe LexicalAnalyzer."""

import pytest

from baobab_geek_interpreter.lexical.lexical_analyzer import LexicalAnalyzer
from baobab_geek_interpreter.lexical.token_type import TokenType


class TestLexicalAnalyzerServiceCalls:
    """Tests d'intégration pour les appels de service."""

    def test_simple_service_call_no_args(self) -> None:
        """Test un appel de service sans arguments."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("myService()")

        assert len(tokens) == 4
        assert tokens[0].type == TokenType.IDENTIFIANT
        assert tokens[0].value == "myService"
        assert tokens[1].type == TokenType.LPAREN
        assert tokens[2].type == TokenType.RPAREN
        assert tokens[3].type == TokenType.EOF

    def test_service_call_with_integer_arg(self) -> None:
        """Test un appel de service avec un argument entier."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("calculate(42)")

        assert len(tokens) == 5
        assert tokens[0].type == TokenType.IDENTIFIANT
        assert tokens[0].value == "calculate"
        assert tokens[1].type == TokenType.LPAREN
        assert tokens[2].type == TokenType.INT
        assert tokens[2].value == 42
        assert tokens[3].type == TokenType.RPAREN
        assert tokens[4].type == TokenType.EOF

    def test_service_call_with_multiple_args(self) -> None:
        """Test un appel de service avec plusieurs arguments."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze('add(10, 20, "result")')

        assert len(tokens) == 9  # add, (, 10, ,, 20, ,, "result", ), EOF
        assert tokens[0].value == "add"
        assert tokens[2].value == 10
        assert tokens[3].type == TokenType.COMMA
        assert tokens[4].value == 20
        assert tokens[5].type == TokenType.COMMA
        assert tokens[6].value == "result"

    def test_service_call_with_negative_numbers(self) -> None:
        """Test un appel de service avec des nombres négatifs."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("subtract(-5, -10)")

        assert len(tokens) == 7  # subtract, (, -5, ,, -10, ), EOF
        assert tokens[2].type == TokenType.INT
        assert tokens[2].value == -5
        assert tokens[4].type == TokenType.INT
        assert tokens[4].value == -10

    def test_service_call_with_float_args(self) -> None:
        """Test un appel de service avec des arguments flottants."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("calculatePi(3.14159, 2.71828)")

        assert len(tokens) == 7  # calculatePi, (, 3.14159, ,, 2.71828, ), EOF
        assert tokens[2].type == TokenType.FLOAT
        assert tokens[2].value == 3.14159
        assert tokens[4].type == TokenType.FLOAT
        assert tokens[4].value == 2.71828


class TestLexicalAnalyzerArrays:
    """Tests d'intégration pour les tableaux."""

    def test_empty_array(self) -> None:
        """Test un tableau vide."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("[]")

        assert len(tokens) == 3
        assert tokens[0].type == TokenType.LBRACKET
        assert tokens[1].type == TokenType.RBRACKET
        assert tokens[2].type == TokenType.EOF

    def test_array_of_integers(self) -> None:
        """Test un tableau d'entiers."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("[1, 2, 3]")

        assert len(tokens) == 8
        assert tokens[0].type == TokenType.LBRACKET
        assert tokens[1].type == TokenType.INT
        assert tokens[1].value == 1
        assert tokens[2].type == TokenType.COMMA
        assert tokens[3].type == TokenType.INT
        assert tokens[3].value == 2
        assert tokens[4].type == TokenType.COMMA
        assert tokens[5].type == TokenType.INT
        assert tokens[5].value == 3
        assert tokens[6].type == TokenType.RBRACKET

    def test_array_of_strings(self) -> None:
        """Test un tableau de chaînes."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze('["hello", "world"]')

        assert len(tokens) == 6
        assert tokens[1].type == TokenType.STRING
        assert tokens[1].value == "hello"
        assert tokens[3].type == TokenType.STRING
        assert tokens[3].value == "world"

    def test_array_of_floats(self) -> None:
        """Test un tableau de flottants."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("[1.5, 2.5, 3.5]")

        assert len(tokens) == 8
        assert tokens[1].type == TokenType.FLOAT
        assert tokens[1].value == 1.5
        assert tokens[3].type == TokenType.FLOAT
        assert tokens[3].value == 2.5
        assert tokens[5].type == TokenType.FLOAT
        assert tokens[5].value == 3.5

    def test_service_call_with_array_arg(self) -> None:
        """Test un appel de service avec un tableau comme argument."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("processArray([1, 2, 3])")

        assert len(tokens) == 11
        assert tokens[0].value == "processArray"
        assert tokens[2].type == TokenType.LBRACKET
        assert tokens[8].type == TokenType.RBRACKET


class TestLexicalAnalyzerWhitespace:
    """Tests d'intégration pour la gestion des espaces."""

    def test_multiple_spaces_between_tokens(self) -> None:
        """Test plusieurs espaces entre tokens."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("func   (   42   )")

        assert len(tokens) == 5
        assert tokens[0].type == TokenType.IDENTIFIANT
        assert tokens[1].type == TokenType.LPAREN
        assert tokens[2].type == TokenType.INT
        assert tokens[3].type == TokenType.RPAREN

    def test_tabs_and_newlines(self) -> None:
        """Test tabulations et nouvelles lignes."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("func\t(\n42\n)")

        assert len(tokens) == 5
        assert tokens[0].type == TokenType.IDENTIFIANT
        assert tokens[2].type == TokenType.INT

    def test_no_spaces_between_delimiters(self) -> None:
        """Test sans espaces entre délimiteurs."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("func()")

        assert len(tokens) == 4

    def test_spaces_preserved_in_strings(self) -> None:
        """Test que les espaces sont préservés dans les chaînes."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze('"hello   world"')

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello   world"


class TestLexicalAnalyzerComplexScenarios:
    """Tests d'intégration pour des scénarios complexes."""

    def test_complex_service_call(self) -> None:
        """Test un appel de service complexe avec divers types."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze('myService(42, 3.14, "hello", [1, 2, 3])')

        # Vérifier quelques tokens clés
        assert tokens[0].value == "myService"
        assert tokens[2].value == 42
        assert tokens[4].value == 3.14
        assert tokens[6].value == "hello"
        assert tokens[8].type == TokenType.LBRACKET

    def test_multiple_service_calls_on_separate_lines(self) -> None:
        """Test plusieurs appels sur des lignes séparées (pour futur usage)."""
        analyzer = LexicalAnalyzer()
        source = """func1(10)
func2(20)"""
        tokens = analyzer.analyze(source)

        # Premier appel
        assert tokens[0].value == "func1"
        assert tokens[0].line == 1
        assert tokens[2].value == 10

        # Deuxième appel
        assert tokens[4].value == "func2"
        assert tokens[4].line == 2
        assert tokens[6].value == 20

    def test_nested_arrays(self) -> None:
        """Test des crochets imbriqués (pour la structure, pas le contenu)."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("[[1, 2], [3, 4]]")

        # Vérifier la structure des tokens (pas la sémantique)
        assert tokens[0].type == TokenType.LBRACKET
        assert tokens[1].type == TokenType.LBRACKET
        # Note : la validation sémantique (tableaux imbriqués interdits)
        # sera faite par l'analyseur sémantique

    def test_string_with_all_escape_sequences(self) -> None:
        """Test une chaîne avec toutes les séquences d'échappement."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze(r'"quote: \" slash: \\ newline: \n tab: \t"')

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.STRING
        assert '"' in tokens[0].value
        assert "\\" in tokens[0].value
        assert "\n" in tokens[0].value
        assert "\t" in tokens[0].value

    def test_identifiers_with_various_conventions(self) -> None:
        """Test identifiants avec différentes conventions de nommage."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("camelCase snake_case _private CONSTANT")

        assert tokens[0].value == "camelCase"
        assert tokens[1].value == "snake_case"
        assert tokens[2].value == "_private"
        assert tokens[3].value == "CONSTANT"

    def test_mixed_positive_and_negative_numbers(self) -> None:
        """Test mélange de nombres positifs et négatifs."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("func(10, -20, 3.5, -4.5)")

        assert tokens[2].value == 10
        assert tokens[4].value == -20
        assert tokens[6].value == 3.5
        assert tokens[8].value == -4.5


class TestLexicalAnalyzerEdgeCases:
    """Tests d'intégration pour les cas limites."""

    def test_single_character_string(self) -> None:
        """Test une chaîne d'un seul caractère."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze('"a"')

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "a"

    def test_very_long_identifier(self) -> None:
        """Test un identifiant très long."""
        analyzer = LexicalAnalyzer()
        long_name = "a" * 100
        tokens = analyzer.analyze(long_name)

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.IDENTIFIANT
        assert tokens[0].value == long_name

    def test_very_large_number(self) -> None:
        """Test un très grand nombre."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("999999999999")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.INT
        assert tokens[0].value == 999999999999

    def test_many_decimal_places(self) -> None:
        """Test un nombre avec beaucoup de décimales."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("3.14159265358979323846")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.FLOAT
        assert tokens[0].value == 3.14159265358979323846

    def test_consecutive_delimiters(self) -> None:
        """Test délimiteurs consécutifs sans espaces."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("()()")

        assert len(tokens) == 5
        assert tokens[0].type == TokenType.LPAREN
        assert tokens[1].type == TokenType.RPAREN
        assert tokens[2].type == TokenType.LPAREN
        assert tokens[3].type == TokenType.RPAREN

    def test_array_with_no_spaces(self) -> None:
        """Test tableau sans espaces."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("[1,2,3]")

        assert len(tokens) == 8
        assert tokens[1].value == 1
        assert tokens[3].value == 2
        assert tokens[5].value == 3
