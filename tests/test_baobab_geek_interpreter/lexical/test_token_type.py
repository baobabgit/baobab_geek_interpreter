"""Tests unitaires pour TokenType."""

from baobab_geek_interpreter.lexical.token_type import TokenType


class TestTokenType:
    """Tests pour l'énumération TokenType."""

    def test_token_type_int_exists(self) -> None:
        """Vérifie que le type INT existe."""
        assert hasattr(TokenType, "INT")

    def test_token_type_float_exists(self) -> None:
        """Vérifie que le type FLOAT existe."""
        assert hasattr(TokenType, "FLOAT")

    def test_token_type_string_exists(self) -> None:
        """Vérifie que le type STRING existe."""
        assert hasattr(TokenType, "STRING")

    def test_token_type_identifiant_exists(self) -> None:
        """Vérifie que le type IDENTIFIANT existe."""
        assert hasattr(TokenType, "IDENTIFIANT")

    def test_token_type_lparen_exists(self) -> None:
        """Vérifie que le type LPAREN existe."""
        assert hasattr(TokenType, "LPAREN")

    def test_token_type_rparen_exists(self) -> None:
        """Vérifie que le type RPAREN existe."""
        assert hasattr(TokenType, "RPAREN")

    def test_token_type_lbracket_exists(self) -> None:
        """Vérifie que le type LBRACKET existe."""
        assert hasattr(TokenType, "LBRACKET")

    def test_token_type_rbracket_exists(self) -> None:
        """Vérifie que le type RBRACKET existe."""
        assert hasattr(TokenType, "RBRACKET")

    def test_token_type_comma_exists(self) -> None:
        """Vérifie que le type COMMA existe."""
        assert hasattr(TokenType, "COMMA")

    def test_token_type_eof_exists(self) -> None:
        """Vérifie que le type EOF existe."""
        assert hasattr(TokenType, "EOF")

    def test_token_type_values_are_unique(self) -> None:
        """Vérifie que chaque type a une valeur unique."""
        values = [member.value for member in TokenType]
        assert len(values) == len(set(values))

    def test_token_type_can_be_compared(self) -> None:
        """Vérifie que les types peuvent être comparés."""
        assert TokenType.INT == TokenType.INT
        assert TokenType.INT != TokenType.FLOAT

    def test_token_type_str_representation(self) -> None:
        """Vérifie la représentation en chaîne."""
        assert str(TokenType.INT) == "INT"
        assert str(TokenType.FLOAT) == "FLOAT"
        assert str(TokenType.STRING) == "STRING"

    def test_token_type_can_be_used_in_dict(self) -> None:
        """Vérifie que les types peuvent être utilisés comme clés."""
        token_dict = {
            TokenType.INT: "integer",
            TokenType.FLOAT: "float",
            TokenType.STRING: "string",
        }
        assert token_dict[TokenType.INT] == "integer"
        assert token_dict[TokenType.FLOAT] == "float"

    def test_all_token_types_have_different_values(self) -> None:
        """Vérifie que tous les types ont des valeurs différentes."""
        types = list(TokenType)
        for i, type1 in enumerate(types):
            for type2 in types[i + 1 :]:
                assert type1.value != type2.value
