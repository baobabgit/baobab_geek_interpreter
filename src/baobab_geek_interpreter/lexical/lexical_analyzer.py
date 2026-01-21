"""Module contenant l'analyseur lexical pour le langage geek."""

from typing import List, Optional

from baobab_geek_interpreter.exceptions.lexical_exception import (
    BaobabLexicalAnalyserException,
)
from baobab_geek_interpreter.lexical.token import Token
from baobab_geek_interpreter.lexical.token_type import TokenType


class LexicalAnalyzer:
    """Analyseur lexical pour le langage geek.

    Transforme une chaîne de caractères source en une liste de tokens
    en utilisant des automates finis déterministes pour reconnaître
    les différents types de tokens (INT, FLOAT, STRING, IDENTIFIANT, etc.).

    :Example:
        >>> analyzer = LexicalAnalyzer()
        >>> tokens = analyzer.analyze('myFunction(42, "hello")')
        >>> tokens[0].type
        <TokenType.IDENTIFIANT: 4>
        >>> tokens[1].type
        <TokenType.LPAREN: 5>
    """

    def __init__(self) -> None:
        """Initialise l'analyseur lexical."""
        self._source: str = ""
        self._position: int = 0
        self._line: int = 1
        self._column: int = 1
        self._tokens: List[Token] = []

    def analyze(self, source: str) -> List[Token]:
        """Analyse une chaîne source et retourne la liste des tokens.

        :param source: Chaîne de caractères à analyser.
        :type source: str
        :return: Liste des tokens extraits.
        :rtype: List[Token]
        :raises BaobabLexicalAnalyserException: Si un caractère invalide est rencontré.

        :Example:
            >>> analyzer = LexicalAnalyzer()
            >>> tokens = analyzer.analyze("123")
            >>> len(tokens)
            2
            >>> tokens[0].type
            <TokenType.INT: 1>
            >>> tokens[1].type
            <TokenType.EOF: 10>
        """
        self._source = source
        self._position = 0
        self._line = 1
        self._column = 1
        self._tokens = []

        while self._position < len(self._source):
            # Ignorer les espaces blancs
            if self._current_char().isspace():
                self._skip_whitespace()
                continue

            # Tenter de reconnaître un token
            token = self._next_token()
            if token:
                self._tokens.append(token)
            else:
                # Caractère invalide
                raise BaobabLexicalAnalyserException(
                    f"Caractère invalide '{self._current_char()}'",
                    source=self._source,
                    position=self._position,
                    line=self._line,
                    column=self._column,
                )

        # Ajouter le token EOF
        self._tokens.append(
            Token(
                TokenType.EOF,
                None,
                self._position,
                self._line,
                self._column,
            )
        )

        return self._tokens

    def _current_char(self) -> str:
        """Retourne le caractère courant.

        :return: Caractère courant ou chaîne vide si fin de source.
        :rtype: str
        """
        if self._position < len(self._source):
            return self._source[self._position]
        return ""

    def _peek_char(self, offset: int = 1) -> str:
        """Regarde le caractère à une position future sans avancer.

        :param offset: Décalage par rapport à la position courante.
        :type offset: int
        :return: Caractère à la position future ou chaîne vide.
        :rtype: str
        """
        pos = self._position + offset
        if pos < len(self._source):
            return self._source[pos]
        return ""

    def _advance(self) -> None:
        """Avance d'un caractère dans la source."""
        if self._position < len(self._source):
            if self._source[self._position] == "\n":
                self._line += 1
                self._column = 1
            else:
                self._column += 1
            self._position += 1

    def _skip_whitespace(self) -> None:
        """Ignore tous les espaces blancs consécutifs."""
        while self._position < len(self._source) and self._current_char().isspace():
            self._advance()

    def _next_token(self) -> Optional[Token]:  # pylint: disable=too-many-return-statements
        """Extrait le prochain token de la source.

        :return: Token extrait ou None si aucun token valide.
        :rtype: Optional[Token]
        """
        start_pos = self._position
        start_line = self._line
        start_column = self._column

        # Délimiteurs simples
        char = self._current_char()
        if char == "(":
            self._advance()
            return Token(TokenType.LPAREN, "(", start_pos, start_line, start_column)
        if char == ")":
            self._advance()
            return Token(TokenType.RPAREN, ")", start_pos, start_line, start_column)
        if char == "[":
            self._advance()
            return Token(TokenType.LBRACKET, "[", start_pos, start_line, start_column)
        if char == "]":
            self._advance()
            return Token(TokenType.RBRACKET, "]", start_pos, start_line, start_column)
        if char == ",":
            self._advance()
            return Token(TokenType.COMMA, ",", start_pos, start_line, start_column)

        # Chaîne de caractères
        if char == '"':
            return self._read_string(start_pos, start_line, start_column)

        # Nombre (INT ou FLOAT) ou signe négatif
        if char.isdigit() or (char == "-" and self._peek_char().isdigit()):
            return self._read_number(start_pos, start_line, start_column)

        # Identifiant
        if char.isalpha() or char == "_":
            return self._read_identifier(start_pos, start_line, start_column)

        return None

    def _read_string(self, start_pos: int, start_line: int, start_column: int) -> Token:
        """Lit une chaîne de caractères entre guillemets doubles.

        Gère les séquences d'échappement : \\", \\\\, \\n, \\t

        :param start_pos: Position de départ du token.
        :type start_pos: int
        :param start_line: Ligne de départ du token.
        :type start_line: int
        :param start_column: Colonne de départ du token.
        :type start_column: int
        :return: Token de type STRING.
        :rtype: Token
        :raises BaobabLexicalAnalyserException: Si la chaîne n'est pas fermée.
        """
        self._advance()  # Sauter le guillemet ouvrant
        value = ""

        while self._position < len(self._source):
            char = self._current_char()

            # Guillemet fermant
            if char == '"':
                self._advance()
                return Token(TokenType.STRING, value, start_pos, start_line, start_column)

            # Séquence d'échappement
            if char == "\\":
                self._advance()
                if self._position >= len(self._source):
                    raise BaobabLexicalAnalyserException(
                        "Chaîne de caractères non terminée",
                        source=self._source,
                        position=start_pos,
                        line=start_line,
                        column=start_column,
                    )

                escape_char = self._current_char()
                if escape_char == '"':
                    value += '"'
                elif escape_char == "\\":
                    value += "\\"
                elif escape_char == "n":
                    value += "\n"
                elif escape_char == "t":
                    value += "\t"
                else:
                    raise BaobabLexicalAnalyserException(
                        f"Séquence d'échappement invalide '\\{escape_char}'",
                        source=self._source,
                        position=self._position,
                        line=self._line,
                        column=self._column,
                    )
                self._advance()
            else:
                # Caractère normal
                value += char
                self._advance()

        # Chaîne non fermée
        raise BaobabLexicalAnalyserException(
            "Chaîne de caractères non terminée",
            source=self._source,
            position=start_pos,
            line=start_line,
            column=start_column,
        )

    def _read_number(self, start_pos: int, start_line: int, start_column: int) -> Token:
        """Lit un nombre (INT ou FLOAT).

        Reconnaît les formats : 123, -456, 3.14, -0.5

        :param start_pos: Position de départ du token.
        :type start_pos: int
        :param start_line: Ligne de départ du token.
        :type start_line: int
        :param start_column: Colonne de départ du token.
        :type start_column: int
        :return: Token de type INT ou FLOAT.
        :rtype: Token
        """
        value = ""

        # Signe négatif optionnel
        if self._current_char() == "-":
            value += "-"
            self._advance()

        # Partie entière
        while self._position < len(self._source) and self._current_char().isdigit():
            value += self._current_char()
            self._advance()

        # Vérifier si c'est un float (présence d'un point)
        if self._current_char() == "." and self._peek_char().isdigit():
            value += "."
            self._advance()

            # Partie décimale
            while self._position < len(self._source) and self._current_char().isdigit():
                value += self._current_char()
                self._advance()

            return Token(TokenType.FLOAT, float(value), start_pos, start_line, start_column)

        return Token(TokenType.INT, int(value), start_pos, start_line, start_column)

    def _read_identifier(self, start_pos: int, start_line: int, start_column: int) -> Token:
        """Lit un identifiant.

        Format : [a-zA-Z_][a-zA-Z0-9_]*

        :param start_pos: Position de départ du token.
        :type start_pos: int
        :param start_line: Ligne de départ du token.
        :type start_line: int
        :param start_column: Colonne de départ du token.
        :type start_column: int
        :return: Token de type IDENTIFIANT.
        :rtype: Token
        """
        value = ""

        # Premier caractère : lettre ou underscore
        char = self._current_char()
        if char.isalpha() or char == "_":
            value += char
            self._advance()

        # Caractères suivants : lettres, chiffres ou underscores
        while self._position < len(self._source):
            char = self._current_char()
            if char.isalnum() or char == "_":
                value += char
                self._advance()
            else:
                break

        return Token(TokenType.IDENTIFIANT, value, start_pos, start_line, start_column)
