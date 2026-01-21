"""Baobab Geek Interpreter.

Interpréteur pour le langage 'geek' permettant le développement rapide d'API de services.

:Example:
    >>> from baobab_geek_interpreter import Interpreter, service
    >>>
    >>> # Définir des services
    >>> @service
    ... def add(a: int, b: int) -> int:
    ...     return a + b
    >>>
    >>> # Créer l'interpréteur
    >>> interpreter = Interpreter()
    >>> interpreter.register_service("add", add)
    >>>
    >>> # Interpréter et exécuter
    >>> result = interpreter.interpret("add(10, 20)")
    >>> print(result)  # 30
"""

from baobab_geek_interpreter.exceptions.base_exception import (
    BaobabGeekInterpreterException,
)
from baobab_geek_interpreter.exceptions.execution_exception import (
    BaobabExecutionException,
)
from baobab_geek_interpreter.exceptions.lexical_exception import (
    BaobabLexicalAnalyserException,
)
from baobab_geek_interpreter.exceptions.semantic_exception import (
    BaobabSemanticAnalyserException,
)
from baobab_geek_interpreter.exceptions.syntax_exception import (
    BaobabSyntaxAnalyserException,
)
from baobab_geek_interpreter.execution.service_decorator import service
from baobab_geek_interpreter.interpreter import Interpreter

__all__ = [
    "Interpreter",
    "service",
    "BaobabGeekInterpreterException",
    "BaobabLexicalAnalyserException",
    "BaobabSyntaxAnalyserException",
    "BaobabSemanticAnalyserException",
    "BaobabExecutionException",
]

__version__ = "1.0.0"
