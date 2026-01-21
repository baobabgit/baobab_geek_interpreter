"""Module principal de l'interpréteur Baobab Geek."""

from typing import Any

from baobab_geek_interpreter.execution.executor import Executor
from baobab_geek_interpreter.lexical.lexical_analyzer import LexicalAnalyzer
from baobab_geek_interpreter.semantic.semantic_analyzer import SemanticAnalyzer
from baobab_geek_interpreter.semantic.symbol_table import SymbolTable
from baobab_geek_interpreter.syntax.syntax_analyzer import SyntaxAnalyzer


class Interpreter:
    """Interpréteur principal pour le langage Geek.

    Assemble tous les composants (lexer, parser, semantic analyzer, executor)
    pour fournir une interface simple d'utilisation.

    :Example:
        >>> from baobab_geek_interpreter import Interpreter, service
        >>> interpreter = Interpreter()
        >>> @service
        ... def add(a: int, b: int) -> int:
        ...     return a + b
        >>> interpreter.register_service("add", add)
        >>> result = interpreter.interpret("add(10, 20)")
        >>> result
        30
    """

    def __init__(self) -> None:
        """Initialise l'interpréteur avec tous ses composants."""
        self._symbol_table = SymbolTable()
        self._lexer = LexicalAnalyzer()
        self._parser = SyntaxAnalyzer()
        self._semantic_analyzer = SemanticAnalyzer(self._symbol_table)
        self._executor = Executor(self._symbol_table)

    def interpret(self, source: str) -> Any:
        """Interprète une chaîne de code source et retourne le résultat.

        Pipeline complet :
        1. Analyse lexicale (source → tokens)
        2. Analyse syntaxique (tokens → AST)
        3. Analyse sémantique (validation AST)
        4. Exécution (AST → résultat)

        :param source: Code source à interpréter.
        :type source: str
        :return: Résultat de l'exécution du service.
        :rtype: Any
        :raises BaobabLexicalAnalyserException: Si erreur lexicale.
        :raises BaobabSyntaxAnalyserException: Si erreur syntaxique.
        :raises BaobabSemanticAnalyserException: Si erreur sémantique.
        :raises BaobabExecutionException: Si erreur d'exécution.

        :Example:
            >>> interpreter = Interpreter()
            >>> # ... enregistrer des services ...
            >>> result = interpreter.interpret("add(10, 20)")
            >>> result
            30
        """
        # Phase 1 : Analyse lexicale
        tokens = self._lexer.analyze(source)

        # Phase 2 : Analyse syntaxique
        ast = self._parser.parse(tokens)

        # Phase 3 : Analyse sémantique
        self._semantic_analyzer.analyze(ast)

        # Phase 4 : Exécution
        return self._executor.execute(ast)

    def register_service(self, name: str, func: Any) -> None:
        """Enregistre un service dans la table des symboles.

        :param name: Nom du service.
        :type name: str
        :param func: Fonction Python à enregistrer.
        :type func: Any

        :Example:
            >>> interpreter = Interpreter()
            >>> def my_service(x: int) -> int:
            ...     return x * 2
            >>> interpreter.register_service("double", my_service)
        """
        self._symbol_table.register(name, func)

    def register_services(self, module: Any) -> None:
        """Découvre et enregistre automatiquement tous les services d'un module.

        Les services sont identifiés par le décorateur @service.

        :param module: Module Python contenant des services décorés.
        :type module: Any

        :Example:
            >>> import my_services
            >>> interpreter = Interpreter()
            >>> interpreter.register_services(my_services)
        """
        self._symbol_table.discover_services(module)

    def list_services(self) -> list[str]:
        """Liste tous les services enregistrés.

        :return: Liste des noms de services.
        :rtype: list[str]

        :Example:
            >>> interpreter = Interpreter()
            >>> # ... enregistrer des services ...
            >>> interpreter.list_services()
            ['add', 'multiply', 'concat']
        """
        return self._symbol_table.list_services()

    def has_service(self, name: str) -> bool:
        """Vérifie si un service est enregistré.

        :param name: Nom du service à vérifier.
        :type name: str
        :return: True si le service existe, False sinon.
        :rtype: bool

        :Example:
            >>> interpreter = Interpreter()
            >>> interpreter.has_service("add")
            False
            >>> # ... enregistrer "add" ...
            >>> interpreter.has_service("add")
            True
        """
        return self._symbol_table.has(name)

    def clear_services(self) -> None:
        """Supprime tous les services enregistrés.

        :Example:
            >>> interpreter = Interpreter()
            >>> # ... enregistrer des services ...
            >>> interpreter.clear_services()
            >>> interpreter.list_services()
            []
        """
        self._symbol_table.clear()
