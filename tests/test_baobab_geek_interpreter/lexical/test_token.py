"""Tests unitaires pour Token."""

from baobab_geek_interpreter.lexical.token import Token
from baobab_geek_interpreter.lexical.token_type import TokenType


class TestToken:
    """Tests pour la classe Token."""

    def test_token_init_with_int_value(self) -> None:
        """Vérifie l'initialisation avec une valeur entière."""
        token = Token(TokenType.INT, 42, 0, 1, 1)
        assert token.type == TokenType.INT
        assert token.value == 42
        assert token.position == 0
        assert token.line == 1
        assert token.column == 1

    def test_token_init_with_float_value(self) -> None:
        """Vérifie l'initialisation avec une valeur flottante."""
        token = Token(TokenType.FLOAT, 3.14, 5, 1, 6)
        assert token.type == TokenType.FLOAT
        assert token.value == 3.14
        assert token.position == 5
        assert token.line == 1
        assert token.column == 6

    def test_token_init_with_string_value(self) -> None:
        """Vérifie l'initialisation avec une chaîne."""
        token = Token(TokenType.STRING, "hello", 10, 2, 1)
        assert token.type == TokenType.STRING
        assert token.value == "hello"
        assert token.position == 10
        assert token.line == 2
        assert token.column == 1

    def test_token_init_with_none_value(self) -> None:
        """Vérifie l'initialisation avec une valeur None."""
        token = Token(TokenType.LPAREN, None, 0, 1, 1)
        assert token.type == TokenType.LPAREN
        assert token.value is None

    def test_token_repr(self) -> None:
        """Vérifie la représentation technique."""
        token = Token(TokenType.INT, 42, 0, 1, 1)
        expected = "Token(INT, 42, pos=0, line=1, col=1)"
        assert repr(token) == expected

    def test_token_str(self) -> None:
        """Vérifie la représentation lisible."""
        token = Token(TokenType.INT, 42, 0, 1, 1)
        assert str(token) == "INT(42)"

    def test_token_str_with_string_value(self) -> None:
        """Vérifie la représentation avec une chaîne."""
        token = Token(TokenType.STRING, "hello", 0, 1, 1)
        assert str(token) == "STRING('hello')"

    def test_token_equality_same_tokens(self) -> None:
        """Vérifie l'égalité entre tokens identiques."""
        token1 = Token(TokenType.INT, 42, 0, 1, 1)
        token2 = Token(TokenType.INT, 42, 0, 1, 1)
        assert token1 == token2

    def test_token_equality_different_type(self) -> None:
        """Vérifie l'inégalité avec des types différents."""
        token1 = Token(TokenType.INT, 42, 0, 1, 1)
        token2 = Token(TokenType.FLOAT, 42, 0, 1, 1)
        assert token1 != token2

    def test_token_equality_different_value(self) -> None:
        """Vérifie l'inégalité avec des valeurs différentes."""
        token1 = Token(TokenType.INT, 42, 0, 1, 1)
        token2 = Token(TokenType.INT, 43, 0, 1, 1)
        assert token1 != token2

    def test_token_equality_different_position(self) -> None:
        """Vérifie l'inégalité avec des positions différentes."""
        token1 = Token(TokenType.INT, 42, 0, 1, 1)
        token2 = Token(TokenType.INT, 42, 5, 1, 1)
        assert token1 != token2

    def test_token_equality_different_line(self) -> None:
        """Vérifie l'inégalité avec des lignes différentes."""
        token1 = Token(TokenType.INT, 42, 0, 1, 1)
        token2 = Token(TokenType.INT, 42, 0, 2, 1)
        assert token1 != token2

    def test_token_equality_different_column(self) -> None:
        """Vérifie l'inégalité avec des colonnes différentes."""
        token1 = Token(TokenType.INT, 42, 0, 1, 1)
        token2 = Token(TokenType.INT, 42, 0, 1, 2)
        assert token1 != token2

    def test_token_equality_with_non_token(self) -> None:
        """Vérifie l'inégalité avec un non-token."""
        token = Token(TokenType.INT, 42, 0, 1, 1)
        assert token != 42
        assert token != "token"
        assert token != None

    def test_token_attributes_are_mutable(self) -> None:
        """Vérifie que les attributs peuvent être modifiés."""
        token = Token(TokenType.INT, 42, 0, 1, 1)
        token.value = 43
        assert token.value == 43
        token.position = 5
        assert token.position == 5

    def test_token_with_large_position_values(self) -> None:
        """Vérifie avec de grandes valeurs de position."""
        token = Token(TokenType.INT, 42, 999999, 1000, 500)
        assert token.position == 999999
        assert token.line == 1000
        assert token.column == 500

    def test_token_with_negative_int(self) -> None:
        """Vérifie avec un entier négatif."""
        token = Token(TokenType.INT, -42, 0, 1, 1)
        assert token.value == -42

    def test_token_with_negative_float(self) -> None:
        """Vérifie avec un flottant négatif."""
        token = Token(TokenType.FLOAT, -3.14, 0, 1, 1)
        assert token.value == -3.14

    def test_token_with_empty_string(self) -> None:
        """Vérifie avec une chaîne vide."""
        token = Token(TokenType.STRING, "", 0, 1, 1)
        assert token.value == ""

    def test_token_with_multiline_string_value(self) -> None:
        """Vérifie avec une chaîne contenant des retours à la ligne."""
        token = Token(TokenType.STRING, "hello\\nworld", 0, 1, 1)
        assert token.value == "hello\\nworld"
