"""Tests unitaires pour la classe LexicalAnalyzer."""

import pytest

from baobab_geek_interpreter.exceptions.lexical_exception import (
    BaobabLexicalAnalyserException,
)
from baobab_geek_interpreter.lexical.lexical_analyzer import LexicalAnalyzer
from baobab_geek_interpreter.lexical.token_type import TokenType


class TestLexicalAnalyzerBasics:
    """Tests de base pour LexicalAnalyzer."""

    def test_analyzer_creation(self) -> None:
        """Test la création d'un analyseur lexical."""
        analyzer = LexicalAnalyzer()
        assert analyzer is not None

    def test_analyze_empty_string(self) -> None:
        """Test l'analyse d'une chaîne vide."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("")

        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF

    def test_analyze_whitespace_only(self) -> None:
        """Test l'analyse d'une chaîne avec seulement des espaces."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("   \n\t  ")

        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF


class TestLexicalAnalyzerIntegers:
    """Tests pour la reconnaissance des entiers."""

    def test_single_digit(self) -> None:
        """Test un chiffre unique."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("5")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.INT
        assert tokens[0].value == 5
        assert tokens[1].type == TokenType.EOF

    def test_multiple_digits(self) -> None:
        """Test un nombre à plusieurs chiffres."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("123")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.INT
        assert tokens[0].value == 123

    def test_negative_integer(self) -> None:
        """Test un entier négatif."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("-456")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.INT
        assert tokens[0].value == -456

    def test_zero(self) -> None:
        """Test le nombre zéro."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("0")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.INT
        assert tokens[0].value == 0


class TestLexicalAnalyzerFloats:
    """Tests pour la reconnaissance des flottants."""

    def test_simple_float(self) -> None:
        """Test un flottant simple."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("3.14")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.FLOAT
        assert tokens[0].value == 3.14

    def test_negative_float(self) -> None:
        """Test un flottant négatif."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("-2.5")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.FLOAT
        assert tokens[0].value == -2.5

    def test_float_with_leading_zero(self) -> None:
        """Test un flottant avec zéro initial."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("0.5")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.FLOAT
        assert tokens[0].value == 0.5

    def test_float_with_many_decimals(self) -> None:
        """Test un flottant avec plusieurs décimales."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("123.456789")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.FLOAT
        assert tokens[0].value == 123.456789


class TestLexicalAnalyzerStrings:
    """Tests pour la reconnaissance des chaînes de caractères."""

    def test_simple_string(self) -> None:
        """Test une chaîne simple."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze('"hello"')

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello"

    def test_empty_string(self) -> None:
        """Test une chaîne vide."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze('""')

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == ""

    def test_string_with_spaces(self) -> None:
        """Test une chaîne avec des espaces."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze('"hello world"')

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello world"

    def test_string_with_escaped_quote(self) -> None:
        """Test une chaîne avec guillemet échappé."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze(r'"say \"hello\""')

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == 'say "hello"'

    def test_string_with_escaped_backslash(self) -> None:
        """Test une chaîne avec backslash échappé."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze(r'"path\\to\\file"')

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == r"path\to\file"

    def test_string_with_escaped_newline(self) -> None:
        """Test une chaîne avec newline échappé."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze(r'"line1\nline2"')

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "line1\nline2"

    def test_string_with_escaped_tab(self) -> None:
        """Test une chaîne avec tab échappé."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze(r'"col1\tcol2"')

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "col1\tcol2"

    def test_string_not_closed_raises_error(self) -> None:
        """Test qu'une chaîne non fermée lève une exception."""
        analyzer = LexicalAnalyzer()

        with pytest.raises(BaobabLexicalAnalyserException, match="non terminée"):
            analyzer.analyze('"hello')

    def test_string_with_invalid_escape_raises_error(self) -> None:
        """Test qu'une séquence d'échappement invalide lève une exception."""
        analyzer = LexicalAnalyzer()

        with pytest.raises(BaobabLexicalAnalyserException, match="échappement invalide"):
            analyzer.analyze(r'"test\x"')


class TestLexicalAnalyzerIdentifiers:
    """Tests pour la reconnaissance des identifiants."""

    def test_simple_identifier(self) -> None:
        """Test un identifiant simple."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("myVar")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.IDENTIFIANT
        assert tokens[0].value == "myVar"

    def test_identifier_with_underscore(self) -> None:
        """Test un identifiant avec underscore."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("my_var")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.IDENTIFIANT
        assert tokens[0].value == "my_var"

    def test_identifier_starting_with_underscore(self) -> None:
        """Test un identifiant commençant par underscore."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("_private")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.IDENTIFIANT
        assert tokens[0].value == "_private"

    def test_identifier_with_digits(self) -> None:
        """Test un identifiant avec des chiffres."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("var123")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.IDENTIFIANT
        assert tokens[0].value == "var123"

    def test_identifier_camel_case(self) -> None:
        """Test un identifiant en CamelCase."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("MyClassName")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.IDENTIFIANT
        assert tokens[0].value == "MyClassName"

    def test_single_letter_identifier(self) -> None:
        """Test un identifiant d'une seule lettre."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("x")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.IDENTIFIANT
        assert tokens[0].value == "x"


class TestLexicalAnalyzerDelimiters:
    """Tests pour la reconnaissance des délimiteurs."""

    def test_left_parenthesis(self) -> None:
        """Test la parenthèse ouvrante."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("(")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.LPAREN
        assert tokens[0].value == "("

    def test_right_parenthesis(self) -> None:
        """Test la parenthèse fermante."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze(")")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.RPAREN
        assert tokens[0].value == ")"

    def test_left_bracket(self) -> None:
        """Test le crochet ouvrant."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("[")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.LBRACKET
        assert tokens[0].value == "["

    def test_right_bracket(self) -> None:
        """Test le crochet fermant."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("]")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.RBRACKET
        assert tokens[0].value == "]"

    def test_comma(self) -> None:
        """Test la virgule."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze(",")

        assert len(tokens) == 2
        assert tokens[0].type == TokenType.COMMA
        assert tokens[0].value == ","


class TestLexicalAnalyzerErrors:
    """Tests pour la gestion des erreurs."""

    def test_invalid_character_raises_error(self) -> None:
        """Test qu'un caractère invalide lève une exception."""
        analyzer = LexicalAnalyzer()

        with pytest.raises(BaobabLexicalAnalyserException, match="Caractère invalide"):
            analyzer.analyze("@")

    def test_error_contains_position_info(self) -> None:
        """Test que l'exception contient les informations de position."""
        analyzer = LexicalAnalyzer()

        try:
            analyzer.analyze("abc @ def")
        except BaobabLexicalAnalyserException as e:
            assert e.line == 1
            assert e.column == 5
            assert e.position == 4
        else:
            pytest.fail("Expected BaobabLexicalAnalyserException")


class TestLexicalAnalyzerPositioning:
    """Tests pour le suivi de position, ligne et colonne."""

    def test_token_positions_single_line(self) -> None:
        """Test les positions des tokens sur une seule ligne."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("abc 123")

        assert tokens[0].position == 0
        assert tokens[0].line == 1
        assert tokens[0].column == 1

        assert tokens[1].position == 4
        assert tokens[1].line == 1
        assert tokens[1].column == 5

    def test_token_positions_multiple_lines(self) -> None:
        """Test les positions des tokens sur plusieurs lignes."""
        analyzer = LexicalAnalyzer()
        tokens = analyzer.analyze("abc\n123")

        assert tokens[0].position == 0
        assert tokens[0].line == 1
        assert tokens[0].column == 1

        assert tokens[1].position == 4
        assert tokens[1].line == 2
        assert tokens[1].column == 1
