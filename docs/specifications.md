# Cahier des Charges - Baobab Geek Interpreter v1.0

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Objectifs](#objectifs)
3. [Fonctionnement général](#fonctionnement-général)
4. [Grammaire formelle](#grammaire-formelle)
5. [Contraintes et règles](#contraintes-et-règles)
6. [Architecture technique](#architecture-technique)
7. [Gestion des exceptions](#gestion-des-exceptions)
8. [Analyseurs](#analyseurs)
9. [Spécifications détaillées](#spécifications-détaillées)
10. [Exemples d'utilisation](#exemples-dutilisation)

---

## Vue d'ensemble

Le **Baobab Geek Interpreter** est une bibliothèque Python permettant le développement rapide d'API de services. Un service est une méthode Python décorée avec le décorateur `@service`. L'interpréteur analyse et exécute des appels de services écrits dans un langage simple appelé "geek".

### Principe de fonctionnement

1. Au démarrage de l'API, la bibliothèque récupère toutes les méthodes décorées avec `@service`
2. Ces méthodes sont ajoutées dans une table des symboles
3. L'utilisateur peut appeler ces services via une chaîne de caractères
4. L'interpréteur analyse et exécute l'appel, puis retourne le résultat

---

## Objectifs

### Objectifs principaux

- Permettre l'appel de services Python via une syntaxe simple et textuelle
- Fournir une analyse complète (lexicale, syntaxique, sémantique) avant l'exécution
- Garantir la sécurité par validation stricte des types
- Offrir des messages d'erreur clairs et précis

### Objectifs de la version 1.0

- ✅ Appels de services avec arguments positionnels
- ✅ Support des types de base : `int`, `float`, `str`, `list`
- ✅ Validation stricte des types d'arguments
- ✅ Tableaux homogènes de constantes
- ✅ Gestion robuste des erreurs avec hiérarchie d'exceptions
- ❌ Pas de chaînage d'appels (prévu v1.1+)
- ❌ Pas d'arguments nommés (prévu v1.1+)
- ❌ Pas de tableaux imbriqués (prévu v1.1+)

---

## Fonctionnement général

### Interface principale

La bibliothèque expose une classe `Interpreter` avec une méthode principale :

```python
def interpret(self, source: str) -> Any:
    """
    Analyse et exécute une chaîne source.
    
    Args:
        source: Code source à interpréter (ex: "add(1, 2)")
        
    Returns:
        Résultat de l'exécution du service
        
    Raises:
        BaobabGeekInterpreterException: En cas d'erreur
    """
```

### Pipeline d'exécution

```
Chaîne source
    ↓
[1] Analyseur Lexical → Liste de tokens
    ↓
[2] Analyseur Syntaxique → Arbre Syntaxique Abstrait (AST)
    ↓
[3] Analyseur Sémantique → Validation
    ↓
[4] Exécuteur → Résultat
```

---

## Grammaire formelle

### Notation BNF

```bnf
axiom             → appel_service

appel_service     → IDENTIFIANT '(' liste_arguments ')'

liste_arguments   → ε
                  | argument (',' argument)*

argument          → constante

constante         → INT
                  | FLOAT
                  | STRING
                  | tableau

tableau           → '[' liste_valeurs ']'

liste_valeurs     → ε
                  | constante (',' constante)*
```

### Tokens (unités lexicales)

```bnf
IDENTIFIANT       → [a-zA-Z_][a-zA-Z0-9_]*
INT               → -?[0-9]+
FLOAT             → -?[0-9]+\.[0-9]+
STRING            → " (CHAR | ESCAPE)* "
CHAR              → [^"\\]
ESCAPE            → \\ | \" | \n | \t
LPAREN            → '('
RPAREN            → ')'
LBRACKET          → '['
RBRACKET          → ']'
COMMA             → ','
WHITESPACE        → [ \t\r\n]+ (ignoré par l'analyseur lexical)
```

### Exemples de syntaxe valide

```python
service()                           # Service sans arguments
add(1, 2)                          # Entiers
divide(10.5, 2.0)                  # Flottants
greet("Hello")                     # Chaîne de caractères
sum_array([1, 2, 3, 4, 5])        # Tableau d'entiers
process("test", 42, [1.0, 2.5])   # Arguments mixtes
empty_list([])                     # Tableau vide
```

### Exemples de syntaxe invalide

```python
add(1, 2.0)                        # Types mixtes sans conversion
sum([1, 2.5])                      # Tableau hétérogène
nested([[1, 2]])                   # Tableaux imbriqués (v1.1+)
chain(add(1, 2))                   # Chaînage (v1.1+)
service(param=value)               # Arguments nommés (v1.1+)
```

---

## Contraintes et règles

### Contraintes de la version 1.0

| Fonctionnalité | Supporté | Notes |
|----------------|----------|-------|
| Arguments positionnels | ✅ | Uniquement |
| Arguments nommés | ❌ | Prévu v1.1+ |
| Types de base (int, float, str) | ✅ | Complet |
| Tableaux homogènes | ✅ | Un seul type par tableau |
| Tableaux vides | ✅ | Type indéterminé |
| Tableaux imbriqués | ❌ | Prévu v1.1+ |
| Chaînage d'appels | ❌ | Prévu v1.1+ |
| Nombres négatifs | ✅ | Le `-` fait partie du littéral |
| Notation scientifique | ❌ | Pas en v1.0 |
| Échappement dans strings | ✅ | `\"`, `\\`, `\n`, `\t` |
| Services sans arguments | ✅ | Syntaxe : `service()` |
| Validation de types | ✅ | Stricte |
| Contexte partagé | ❌ | Exécution pure |

### Règles sémantiques

1. **Service existant** : Le service appelé doit être enregistré dans la table des symboles
2. **Nombre d'arguments** : Le nombre d'arguments doit correspondre à la signature du service
3. **Types d'arguments** : Les types doivent correspondre exactement (validation stricte)
4. **Homogénéité des tableaux** : Tous les éléments d'un tableau doivent être du même type
5. **Pas d'imbrication** : Les tableaux ne peuvent pas contenir d'autres tableaux (v1.0)

### Règles d'échappement pour les chaînes

| Séquence | Résultat | Description |
|----------|----------|-------------|
| `\"` | `"` | Guillemet double |
| `\\` | `\` | Backslash |
| `\n` | Saut de ligne | Nouvelle ligne |
| `\t` | Tabulation | Tabulation horizontale |

Exemple : `"He said \"Hello\"\nNext line"` → `He said "Hello"` + saut de ligne + `Next line`

### Gestion des espaces

Les espaces, tabulations et sauts de ligne sont ignorés par l'analyseur lexical, sauf :
- À l'intérieur des chaînes de caractères
- Entre les chiffres d'un nombre (interdit)

Toutes ces formes sont équivalentes :

```python
service(1,2,3)
service( 1, 2, 3 )
service(  1  ,  2  ,  3  )
service(
    1,
    2,
    3
)
```

---

## Architecture technique

### Structure des modules

```
src/baobab_geek_interpreter/
├── __init__.py
├── interpreter.py                    # Interface principale
│
├── exceptions/
│   ├── __init__.py
│   ├── base_exception.py            # BaobabGeekInterpreterException
│   ├── lexical_exception.py         # BaobabLexicalAnalyserException
│   ├── syntax_exception.py          # BaobabSyntaxAnalyserException
│   ├── semantic_exception.py        # BaobabSemanticAnalyserException
│   └── execution_exception.py       # BaobabExecutionException
│
├── lexical/
│   ├── __init__.py
│   ├── token.py                     # Classe Token
│   ├── token_type.py                # Enum TokenType
│   ├── automaton/
│   │   ├── __init__.py
│   │   ├── state.py                 # Classe State
│   │   ├── transition.py            # Classe Transition
│   │   └── automaton.py             # Classe Automaton
│   └── lexical_analyzer.py          # Analyseur lexical
│
├── syntax/
│   ├── __init__.py
│   ├── ast_node.py                  # Classes AST (base + spécialisées)
│   └── syntax_analyzer.py           # Analyseur syntaxique
│
├── semantic/
│   ├── __init__.py
│   ├── symbol_table.py              # Table des symboles
│   ├── type_checker.py              # Vérification de types
│   └── semantic_analyzer.py         # Analyseur sémantique
│
└── execution/
    ├── __init__.py
    ├── service_decorator.py         # Décorateur @service
    └── executor.py                  # Exécuteur (visiteur AST)
```

### Composants principaux

#### 1. Interpreter
Interface principale exposant la méthode `interpret(source: str) -> Any`.

#### 2. LexicalAnalyzer
Transforme une chaîne de caractères en liste de tokens à l'aide d'automates finis déterministes.

#### 3. SyntaxAnalyzer
Construit un Arbre Syntaxique Abstrait (AST) à partir de la liste de tokens, en suivant la grammaire BNF.

#### 4. SemanticAnalyzer
Valide l'AST :
- Vérifie l'existence du service
- Valide le nombre d'arguments
- Vérifie les types d'arguments
- Valide l'homogénéité des tableaux

#### 5. Executor
Parcourt l'AST et exécute le service avec les arguments fournis.

---

## Gestion des exceptions

### Hiérarchie

```
BaobabGeekInterpreterException (base)
├── BaobabLexicalAnalyserException
├── BaobabSyntaxAnalyserException
├── BaobabSemanticAnalyserException
└── BaobabExecutionException
```

### Informations contextuelles

Toutes les exceptions héritent de `BaobabGeekInterpreterException` et contiennent :

```python
class BaobabGeekInterpreterException(Exception):
    message: str           # Message d'erreur
    source: str | None     # Code source complet
    position: int | None   # Position du caractère dans la source
    line: int | None       # Numéro de ligne
    column: int | None     # Numéro de colonne
```

### Gestion des exceptions des services

Si un service Python lève une exception, elle est encapsulée dans `BaobabExecutionException` :

```python
class BaobabExecutionException(BaobabGeekInterpreterException):
    service_name: str                    # Nom du service
    original_exception: Exception | None # Exception d'origine
```

Exemple :
```python
@service
def divide(a: int, b: int) -> float:
    return a / b

# Appel : interpret("divide(10, 0)")
# Lève : BaobabExecutionException(
#     message="Error executing service 'divide': division by zero",
#     service_name="divide",
#     original_exception=ZeroDivisionError(...)
# )
```

---

## Analyseurs

### 1. Analyseur Lexical

#### Objectifs
- Lire le texte source caractère par caractère
- Éliminer les informations inutiles (espaces non significatifs)
- Détecter et traiter les erreurs
- Regrouper les caractères en unités lexicales (tokens)

#### Automates finis déterministes

Pour identifier les unités lexicales, on utilise des automates finis déterministes définis par le quadruplet **(E, e₀, TT, ES)** où :

- **E** : Ensemble des états
- **e₀** : État initial (e₀ ∈ E)
- **TT** : Fonction de transition (TT : E × V → E où V est le vocabulaire)
- **ES** : Ensemble des états de satisfaction (ES ⊆ E)

#### Classes de l'automate

```python
class State:
    """Représente un état de l'automate."""
    name: str
    is_final: bool

class Transition:
    """Représente une transition entre deux états."""
    from_state: State
    to_state: State
    condition: Callable[[str], bool]  # Prédicat sur le caractère

class Automaton:
    """Automate fini déterministe."""
    states: Set[State]
    initial_state: State
    transitions: List[Transition]
    final_states: Set[State]
    
    def process(self, input: str) -> bool
    def get_token_type(self) -> TokenType
```

#### Automates spécifiques

1. **Automate INT** : Reconnaît `-?[0-9]+`
2. **Automate FLOAT** : Reconnaît `-?[0-9]+\.[0-9]+`
3. **Automate STRING** : Reconnaît `"[^"\\]*"` avec échappement
4. **Automate IDENTIFIANT** : Reconnaît `[a-zA-Z_][a-zA-Z0-9_]*`
5. **Automates délimiteurs** : Reconnaissent `(`, `)`, `[`, `]`, `,`

### 2. Analyseur Syntaxique

#### Technique
Parser descendant récursif avec une méthode par règle de grammaire.

#### Méthodes principales
```python
def parse_appel_service() -> ServiceCallNode
def parse_liste_arguments() -> List[ArgumentNode]
def parse_argument() -> ArgumentNode
def parse_constante() -> ConstantNode
def parse_tableau() -> ArrayNode
```

#### Construction de l'AST
Chaque méthode construit un nœud de l'arbre syntaxique abstrait correspondant à sa règle.

### 3. Analyseur Sémantique

#### Vérifications
1. **Existence du service** : Le service doit être dans la table des symboles
2. **Nombre d'arguments** : Correspondance avec la signature
3. **Types d'arguments** : Validation stricte des types
4. **Homogénéité des tableaux** : Tous les éléments du même type

#### TypeChecker
Composant dédié à la validation des types avec conversion si nécessaire :
- `int` → `int` ✅
- `float` → `float` ✅
- `int` → `float` ❌ (strict, pas de conversion automatique)

---

## Spécifications détaillées

### Décorateur @service

```python
def service(func: Callable) -> Callable:
    """
    Décore une fonction pour l'enregistrer comme service.
    
    La fonction décorée est marquée avec l'attribut _is_service = True
    pour permettre sa découverte automatique.
    
    Args:
        func: Fonction à décorer
        
    Returns:
        Fonction décorée avec métadonnées
        
    Example:
        @service
        def add(a: int, b: int) -> int:
            return a + b
    """
    func._is_service = True
    func._service_name = func.__name__
    return func
```

### Table des symboles

```python
class SymbolTable:
    """Gère l'enregistrement et la recherche des services."""
    
    def register(self, name: str, func: Callable) -> None:
        """Enregistre un service."""
        
    def get(self, name: str) -> Callable | None:
        """Récupère un service par son nom."""
        
    def has(self, name: str) -> bool:
        """Vérifie si un service existe."""
        
    def discover_services(self, module: Any) -> None:
        """Découvre et enregistre tous les services d'un module."""
```

### Nœuds de l'AST

```python
# Pattern Visitor pour parcourir l'arbre
class ASTVisitor(ABC):
    @abstractmethod
    def visit_service_call(self, node: ServiceCallNode) -> Any: pass
    
    @abstractmethod
    def visit_argument(self, node: ArgumentNode) -> Any: pass
    
    @abstractmethod
    def visit_int(self, node: IntNode) -> Any: pass
    
    @abstractmethod
    def visit_float(self, node: FloatNode) -> Any: pass
    
    @abstractmethod
    def visit_string(self, node: StringNode) -> Any: pass
    
    @abstractmethod
    def visit_array(self, node: ArrayNode) -> Any: pass
```

### Exécuteur

```python
class Executor(ASTVisitor):
    """Exécute l'AST et retourne le résultat."""
    
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table
    
    def execute(self, ast: ASTNode) -> Any:
        """Point d'entrée pour l'exécution."""
        try:
            return ast.accept(self)
        except BaobabGeekInterpreterException:
            raise
        except Exception as e:
            # Wrapper les exceptions non gérées
            raise BaobabExecutionException(...)
    
    def visit_service_call(self, node: ServiceCallNode) -> Any:
        """Exécute l'appel de service."""
        service = self.symbol_table.get(node.name)
        args = [arg.accept(self) for arg in node.arguments]
        
        try:
            return service(*args)
        except Exception as e:
            raise BaobabExecutionException(
                f"Error executing service '{node.name}': {str(e)}",
                service_name=node.name,
                original_exception=e
            )
```

---

## Exemples d'utilisation

### Exemple basique

```python
from baobab_geek_interpreter import Interpreter, service

# Définir des services
@service
def add(a: int, b: int) -> int:
    """Additionne deux entiers."""
    return a + b

@service
def greet(name: str) -> str:
    """Salue une personne."""
    return f"Hello, {name}!"

# Créer l'interpréteur
interpreter = Interpreter()

# Enregistrer les services (découverte automatique)
import sys
interpreter.register_services(sys.modules[__name__])

# Exécuter des appels
result1 = interpreter.interpret("add(10, 32)")
print(result1)  # 42

result2 = interpreter.interpret("greet(\"World\")")
print(result2)  # Hello, World!
```

### Exemple avec tableaux

```python
@service
def sum_array(numbers: list[int]) -> int:
    """Calcule la somme d'un tableau d'entiers."""
    return sum(numbers)

@service
def average(values: list[float]) -> float:
    """Calcule la moyenne d'un tableau de flottants."""
    return sum(values) / len(values)

result3 = interpreter.interpret("sum_array([1, 2, 3, 4, 5])")
print(result3)  # 15

result4 = interpreter.interpret("average([1.5, 2.5, 3.5])")
print(result4)  # 2.5
```

### Exemple avec gestion d'erreurs

```python
try:
    # Erreur lexicale (string non fermée)
    interpreter.interpret('greet("test)')
except BaobabLexicalAnalyserException as e:
    print(f"Erreur lexicale : {e}")

try:
    # Erreur syntaxique (virgule manquante)
    interpreter.interpret("add(1 2)")
except BaobabSyntaxAnalyserException as e:
    print(f"Erreur syntaxique : {e}")

try:
    # Erreur sémantique (service inexistant)
    interpreter.interpret("unknown_service()")
except BaobabSemanticAnalyserException as e:
    print(f"Erreur sémantique : {e}")

try:
    # Erreur d'exécution (division par zéro)
    @service
    def divide(a: int, b: int) -> float:
        return a / b
    
    interpreter.interpret("divide(10, 0)")
except BaobabExecutionException as e:
    print(f"Erreur d'exécution : {e}")
    print(f"Exception d'origine : {e.original_exception}")
```

### Exemple avec formatage libre

```python
# Toutes ces formes sont valides et équivalentes
result = interpreter.interpret("add(1, 2)")
result = interpreter.interpret("add( 1, 2 )")
result = interpreter.interpret("add(  1  ,  2  )")
result = interpreter.interpret("""
add(
    1,
    2
)
""")
```

---

## Évolutions futures

### Version 1.1
- Support des arguments nommés : `service(param=value)`
- Chaînage d'appels : `service1(service2(42))`
- Tableaux imbriqués : `[[1, 2], [3, 4]]`
- Opérateurs arithmétiques simples : `add(1 + 2, 3 * 4)`

### Version 1.2
- Support des booléens : `true`, `false`
- Support de `null`/`None`
- Opérateurs logiques : `and`, `or`, `not`
- Commentaires dans le code source

### Version 2.0
- Variables et assignation
- Structures de contrôle (if/else, boucles)
- Définition de fonctions dans le langage
- Modules et imports

---

## Conformité

Ce cahier des charges respecte les contraintes définies dans `dev_constraints.md` :
- ✅ Programmation orientée objet (une classe par fichier)
- ✅ Hiérarchie d'exceptions personnalisées
- ✅ Tests unitaires avec couverture ≥ 90%
- ✅ Type hints et annotations complètes
- ✅ Documentation reStructuredText
- ✅ Configuration centralisée dans `pyproject.toml`
- ✅ Standards de nommage PEP 8
- ✅ Versioning sémantique
