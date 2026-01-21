# Baobab Geek Interpreter

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Quality](https://img.shields.io/badge/pylint-10.00%2F10-brightgreen.svg)](https://www.pylint.org/)

**Baobab Geek Interpreter** est une bibliothèque Python permettant de créer rapidement des APIs de services interprétables. Elle fournit un interpréteur complet pour le langage "geek", un langage simple conçu pour l'appel de services avec validation stricte des types.

## 🚀 Caractéristiques

- ✅ **Interpréteur complet** : Analyse lexicale, syntaxique, sémantique et exécution
- ✅ **Validation stricte des types** : Pas de conversion automatique
- ✅ **Décorateur simple** : `@service` pour marquer vos fonctions
- ✅ **Support des tableaux** : Tableaux homogènes de types primitifs
- ✅ **Gestion d'erreurs robuste** : Exceptions détaillées à chaque phase
- ✅ **API intuitive** : Interface simple et documentée
- ✅ **100% testé** : 516 tests unitaires et d'intégration
- ✅ **Qualité irréprochable** : Pylint 10/10, MyPy, Flake8, Bandit

## 📦 Installation

```bash
pip install baobab-geek-interpreter
```

Ou depuis les sources :

```bash
git clone https://github.com/baobabgit/baobab_geek_interpreter.git
cd baobab_geek_interpreter
pip install -e .
```

## 🎯 Quick Start

```python
from baobab_geek_interpreter import Interpreter, service

# 1. Créer l'interpréteur
interpreter = Interpreter()

# 2. Définir des services avec le décorateur @service
@service
def add(a: int, b: int) -> int:
    """Additionne deux nombres."""
    return a + b

@service
def greet(name: str) -> str:
    """Salue une personne."""
    return f"Hello, {name}!"

# 3. Enregistrer les services
interpreter.register_service("add", add)
interpreter.register_service("greet", greet)

# 4. Interpréter et exécuter
result1 = interpreter.interpret("add(10, 20)")
print(result1)  # 30

result2 = interpreter.interpret('greet("Alice")')
print(result2)  # Hello, Alice!
```

## 📚 Documentation

### Types supportés

Le langage "geek" supporte les types suivants :

- **Entiers** : `42`, `-10`
- **Flottants** : `3.14`, `-2.5`
- **Chaînes** : `"hello"`, `"world"`
- **Tableaux** : `[1, 2, 3]`, `["a", "b"]`, `[1.5, 2.5]`

### Grammaire

```bnf
appel_service     → IDENTIFIANT '(' liste_arguments ')'
liste_arguments   → ε | argument (',' argument)*
argument          → constante
constante         → INT | FLOAT | STRING | tableau
tableau           → '[' liste_valeurs ']'
liste_valeurs     → ε | constante (',' constante)*
```

### Exemples d'utilisation

#### Services avec différents types

```python
from baobab_geek_interpreter import Interpreter, service

interpreter = Interpreter()

@service
def multiply(a: float, b: float) -> float:
    return a * b

@service
def concat(a: str, b: str) -> str:
    return a + b

interpreter.register_service("multiply", multiply)
interpreter.register_service("concat", concat)

print(interpreter.interpret("multiply(2.5, 4.0)"))  # 10.0
print(interpreter.interpret('concat("Hello", " World")'))  # Hello World
```

#### Services avec tableaux

```python
@service
def sum_numbers(numbers: list[int]) -> int:
    return sum(numbers)

@service
def join_words(words: list[str], separator: str) -> str:
    return separator.join(words)

interpreter.register_service("sum_numbers", sum_numbers)
interpreter.register_service("join_words", join_words)

print(interpreter.interpret("sum_numbers([1, 2, 3, 4, 5])"))  # 15
print(interpreter.interpret('join_words(["Hello", "World"], " ")'))  # Hello World
```

#### Enregistrement automatique depuis un module

```python
# my_services.py
from baobab_geek_interpreter import service

@service
def add(a: int, b: int) -> int:
    return a + b

@service
def subtract(a: int, b: int) -> int:
    return a - b

# main.py
import my_services
from baobab_geek_interpreter import Interpreter

interpreter = Interpreter()
interpreter.register_services(my_services)

print(interpreter.interpret("add(10, 5)"))       # 15
print(interpreter.interpret("subtract(10, 5)"))  # 5
```

### Gestion des erreurs

L'interpréteur lève des exceptions spécifiques pour chaque phase :

```python
from baobab_geek_interpreter import (
    Interpreter,
    BaobabLexicalAnalyserException,
    BaobabSyntaxAnalyserException,
    BaobabSemanticAnalyserException,
    BaobabExecutionException,
)

interpreter = Interpreter()

try:
    result = interpreter.interpret("unknown_service(42)")
except BaobabSemanticAnalyserException as e:
    print(f"Erreur sémantique : {e}")
    # Erreur sémantique : Service inconnu : 'unknown_service'
```

### API Reference

#### Classe `Interpreter`

**Méthodes principales :**

- `interpret(source: str) -> Any` : Interprète et exécute le code source
- `register_service(name: str, func: Callable) -> None` : Enregistre un service
- `register_services(module: Any) -> None` : Découvre et enregistre les services d'un module
- `list_services() -> list[str]` : Liste tous les services enregistrés
- `has_service(name: str) -> bool` : Vérifie si un service existe
- `clear_services() -> None` : Supprime tous les services

#### Décorateur `@service`

Marque une fonction comme service interprétable. La fonction doit avoir des annotations de type pour la validation.

```python
@service
def my_function(arg1: type1, arg2: type2) -> return_type:
    ...
```

#### Exceptions

- `BaobabGeekInterpreterException` : Exception de base
- `BaobabLexicalAnalyserException` : Erreur lexicale (caractère invalide)
- `BaobabSyntaxAnalyserException` : Erreur syntaxique (syntaxe incorrecte)
- `BaobabSemanticAnalyserException` : Erreur sémantique (service inconnu, types incompatibles)
- `BaobabExecutionException` : Erreur d'exécution (exception dans le service)

## 🛠️ Développement

### Prérequis

- Python 3.10+
- pip

### Installation pour le développement

```bash
git clone https://github.com/baobabgit/baobab_geek_interpreter.git
cd baobab_geek_interpreter
pip install -e ".[dev]"
```

### Exécuter les tests

```bash
# Tous les tests
pytest

# Avec couverture
pytest --cov=src/baobab_geek_interpreter --cov-report=html

# Tests spécifiques
pytest tests/test_baobab_geek_interpreter/test_interpreter.py
```

### Qualité du code

```bash
# Formatage
black src/ tests/

# Linting
pylint src/baobab_geek_interpreter/

# Type checking
mypy src/baobab_geek_interpreter/

# PEP 8
flake8 src/baobab_geek_interpreter/

# Sécurité
bandit -r src/baobab_geek_interpreter/
```

## 📖 Exemples

Consultez le dossier `examples/` pour des exemples complets :

- `basic_usage.py` : Utilisation basique
- `advanced_usage.py` : Cas d'usage avancés
- `error_handling.py` : Gestion des erreurs
- `custom_services.py` : Services personnalisés

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'feat: Add AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Conventions

- Utilisez les [Conventional Commits](https://www.conventionalcommits.org/)
- Maintenez la couverture de tests ≥ 90%
- Respectez Pylint 10/10
- Ajoutez des docstrings pour toutes les fonctions publiques

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- Inspiré par les principes de conception de langages de programmation
- Développé avec ❤️ en Python

## 📞 Contact

- **Auteur** : Baobab Team
- **GitHub** : [baobabgit/baobab_geek_interpreter](https://github.com/baobabgit/baobab_geek_interpreter)
- **Issues** : [GitHub Issues](https://github.com/baobabgit/baobab_geek_interpreter/issues)

## 🗺️ Roadmap

- [ ] Support des tableaux imbriqués (v2.0)
- [ ] Support des types personnalisés (v2.0)
- [ ] Optimisation des performances (v1.1)
- [ ] Plugin pour VS Code (v1.2)
- [ ] Documentation interactive (v1.1)

---

**Version actuelle** : 1.0.0  
**Python** : 3.10+  
**Statut** : Production Ready ✅
