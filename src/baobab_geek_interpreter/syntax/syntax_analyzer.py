"""Module contenant l'analyseur syntaxique pour le langage geek."""

from typing import List

from baobab_geek_interpreter.exceptions.syntax_exception import (
    BaobabSyntaxAnalyserException,
)
from baobab_geek_interpreter.lexical.token import Token
from baobab_geek_interpreter.lexical.token_type import TokenType
from baobab_geek_interpreter.syntax.ast_node import (
    ArgumentNode,
    ArrayNode,
    ConstantNode,
    FloatNode,
    IntNode,
    ServiceCallNode,
    StringNode,
)


class SyntaxAnalyzer:
    """Analyseur syntaxique pour le langage geek.

    Construit un arbre syntaxique abstrait (AST) à partir d'une liste de tokens
    en utilisant un parser descendant récursif. Chaque règle de la grammaire
    correspond à une méthode.

    Grammaire:
        appel_service     → IDENTIFIANT '(' liste_arguments ')'
        liste_arguments   → ε | argument (',' argument)*
        argument          → constante
        constante         → INT | FLOAT | STRING | tableau
        tableau           → '[' liste_valeurs ']'
        liste_valeurs     → ε | constante (',' constante)*

    :Example:
        >>> from baobab_geek_interpreter.lexical.lexical_analyzer import LexicalAnalyzer
        >>> lexer = LexicalAnalyzer()
        >>> tokens = lexer.analyze('myService(42)')
        >>> parser = SyntaxAnalyzer()
        >>> ast = parser.parse(tokens)
        >>> ast.service_name
        'myService'
    """

    def __init__(self) -> None:
        """Initialise l'analyseur syntaxique."""
        self._tokens: List[Token] = []
        self._position: int = 0

    def parse(self, tokens: List[Token]) -> ServiceCallNode:
        """Parse une liste de tokens et retourne l'AST.

        :param tokens: Liste de tokens à analyser.
        :type tokens: List[Token]
        :return: Nœud racine de l'AST (appel de service).
        :rtype: ServiceCallNode
        :raises BaobabSyntaxAnalyserException: Si une erreur syntaxique est détectée.

        :Example:
            >>> from baobab_geek_interpreter.lexical.lexical_analyzer import LexicalAnalyzer
            >>> lexer = LexicalAnalyzer()
            >>> tokens = lexer.analyze('test()')
            >>> parser = SyntaxAnalyzer()
            >>> ast = parser.parse(tokens)
            >>> isinstance(ast, ServiceCallNode)
            True
        """
        self._tokens = tokens
        self._position = 0

        if not self._tokens:
            raise BaobabSyntaxAnalyserException(
                "Liste de tokens vide",
                source="",
                position=0,
                line=1,
                column=1,
            )

        return self._parse_appel_service()

    def _current_token(self) -> Token:
        """Retourne le token courant.

        :return: Token courant.
        :rtype: Token
        :raises BaobabSyntaxAnalyserException: Si on dépasse la fin des tokens.
        """
        if self._position >= len(self._tokens):
            last_token = self._tokens[-1] if self._tokens else None
            raise BaobabSyntaxAnalyserException(
                "Fin inattendue de l'entrée",
                source="",
                position=last_token.position if last_token else 0,
                line=last_token.line if last_token else 1,
                column=last_token.column if last_token else 1,
            )
        return self._tokens[self._position]

    def _peek_token(self, offset: int = 1) -> Token:
        """Regarde le token à une position future sans avancer.

        :param offset: Décalage par rapport à la position courante.
        :type offset: int
        :return: Token à la position future.
        :rtype: Token
        :raises BaobabSyntaxAnalyserException: Si on dépasse la fin des tokens.
        """
        pos = self._position + offset
        if pos >= len(self._tokens):
            last_token = self._tokens[-1] if self._tokens else None
            raise BaobabSyntaxAnalyserException(
                "Fin inattendue de l'entrée",
                source="",
                position=last_token.position if last_token else 0,
                line=last_token.line if last_token else 1,
                column=last_token.column if last_token else 1,
            )
        return self._tokens[pos]

    def _advance(self) -> None:
        """Avance au token suivant."""
        self._position += 1

    def _expect(self, token_type: TokenType) -> Token:
        """Vérifie que le token courant est du type attendu et avance.

        :param token_type: Type de token attendu.
        :type token_type: TokenType
        :return: Token consommé.
        :rtype: Token
        :raises BaobabSyntaxAnalyserException: Si le token n'est pas du type attendu.

        :Example:
            >>> # self._expect(TokenType.LPAREN)  # Attend une parenthèse ouvrante
        """
        token = self._current_token()
        if token.type != token_type:
            raise BaobabSyntaxAnalyserException(
                f"Token inattendu : attendu {token_type.name}, " f"obtenu {token.type.name}",
                source="",
                position=token.position,
                line=token.line,
                column=token.column,
            )
        self._advance()
        return token

    def _parse_appel_service(self) -> ServiceCallNode:
        """Parse un appel de service : IDENTIFIANT '(' liste_arguments ')'.

        :return: Nœud d'appel de service.
        :rtype: ServiceCallNode
        :raises BaobabSyntaxAnalyserException: Si la syntaxe est incorrecte.
        """
        # IDENTIFIANT
        service_token = self._expect(TokenType.IDENTIFIANT)
        service_name = str(service_token.value)

        # '('
        self._expect(TokenType.LPAREN)

        # liste_arguments
        arguments = self._parse_liste_arguments()

        # ')'
        self._expect(TokenType.RPAREN)

        # Vérifier EOF
        if self._current_token().type != TokenType.EOF:
            token = self._current_token()
            raise BaobabSyntaxAnalyserException(
                f"Contenu inattendu après l'appel de service : {token.type.name}",
                source="",
                position=token.position,
                line=token.line,
                column=token.column,
            )

        return ServiceCallNode(service_name, arguments)

    def _parse_liste_arguments(self) -> List[ArgumentNode]:
        """Parse une liste d'arguments : ε | argument (',' argument)*.

        :return: Liste de nœuds d'arguments.
        :rtype: List[ArgumentNode]
        """
        arguments: List[ArgumentNode] = []

        # Vérifier si liste vide (token suivant est ')')
        if self._current_token().type == TokenType.RPAREN:
            return arguments

        # Premier argument
        arguments.append(self._parse_argument())

        # Arguments suivants (',' argument)*
        while self._current_token().type == TokenType.COMMA:
            self._advance()  # Consommer la virgule
            arguments.append(self._parse_argument())

        return arguments

    def _parse_argument(self) -> ArgumentNode:
        """Parse un argument : constante.

        :return: Nœud d'argument.
        :rtype: ArgumentNode
        """
        constante = self._parse_constante()
        return ArgumentNode(constante)

    def _parse_constante(self) -> ConstantNode:
        """Parse une constante : INT | FLOAT | STRING | tableau.

        :return: Nœud de constante.
        :rtype: ConstantNode
        :raises BaobabSyntaxAnalyserException: Si le token n'est pas une constante valide.
        """
        token = self._current_token()

        if token.type == TokenType.INT:
            self._advance()
            return IntNode(int(token.value))

        if token.type == TokenType.FLOAT:
            self._advance()
            return FloatNode(float(token.value))

        if token.type == TokenType.STRING:
            self._advance()
            return StringNode(str(token.value))

        if token.type == TokenType.LBRACKET:
            return self._parse_tableau()

        raise BaobabSyntaxAnalyserException(
            f"Constante attendue, obtenu {token.type.name}",
            source="",
            position=token.position,
            line=token.line,
            column=token.column,
        )

    def _parse_tableau(self) -> ArrayNode:
        """Parse un tableau : '[' liste_valeurs ']'.

        :return: Nœud de tableau.
        :rtype: ArrayNode
        """
        # '['
        self._expect(TokenType.LBRACKET)

        # liste_valeurs
        elements = self._parse_liste_valeurs()

        # ']'
        self._expect(TokenType.RBRACKET)

        return ArrayNode(elements)

    def _parse_liste_valeurs(self) -> List[ConstantNode]:
        """Parse une liste de valeurs : ε | constante (',' constante)*.

        :return: Liste de nœuds de constantes.
        :rtype: List[ConstantNode]
        """
        elements: List[ConstantNode] = []

        # Vérifier si liste vide (token suivant est ']')
        if self._current_token().type == TokenType.RBRACKET:
            return elements

        # Premier élément
        elements.append(self._parse_constante())

        # Éléments suivants (',' constante)*
        while self._current_token().type == TokenType.COMMA:
            self._advance()  # Consommer la virgule
            elements.append(self._parse_constante())

        return elements
