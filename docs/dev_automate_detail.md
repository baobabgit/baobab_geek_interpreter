# 🤖 Développement Détaillé - Phase 3 : Automates Finis Déterministes

## 📘 Vue d'ensemble

La Phase 3 consiste à implémenter un moteur générique d'automates finis déterministes (AFD) qui servira de fondation pour l'analyseur lexical. Ce moteur sera réutilisable, testable et performant.

---

## 🎯 Objectifs

1. **Créer un moteur d'automate générique** : Indépendant du langage "geek", réutilisable pour n'importe quel motif de reconnaissance
2. **Assurer la robustesse** : Gestion d'erreurs, validation des états
3. **Optimiser les performances** : Transitions rapides, recherche efficace
4. **Faciliter les tests** : Architecture claire permettant des tests unitaires exhaustifs

---

## 📚 Concepts Théoriques

### Automate Fini Déterministe (AFD)

Un AFD est un modèle mathématique composé de :

- **Q** : Ensemble fini d'états
- **Σ** : Alphabet (ensemble de symboles d'entrée)
- **δ** : Fonction de transition : Q × Σ → Q
- **q₀** : État initial
- **F** : Ensemble d'états finaux (acceptants)

**Propriété clé du déterminisme** : Pour chaque état et chaque symbole, il existe **au plus une** transition possible.

### Fonctionnement

1. L'automate démarre dans l'état initial `q₀`
2. Pour chaque caractère de l'entrée :
   - Cherche une transition depuis l'état courant qui correspond au caractère
   - Si trouvée : passe à l'état cible
   - Si non trouvée : échec
3. À la fin de l'entrée :
   - Si l'état courant est final : **acceptation**
   - Sinon : **rejet**

### Exemple : Reconnaissance d'un nombre entier positif

```
États : {START, DIGIT, ERROR}
État initial : START
États finaux : {DIGIT}

Transitions :
- START --[0-9]--> DIGIT
- DIGIT --[0-9]--> DIGIT
- START --[autre]--> ERROR
- DIGIT --[autre]--> ERROR
```

**Exemple d'exécution** : `"123"`
- START → (lire '1') → DIGIT
- DIGIT → (lire '2') → DIGIT
- DIGIT → (lire '3') → DIGIT
- Fin d'entrée, état DIGIT est final → **Accepté**

---

## 🏗️ Architecture des Classes

### 1. Classe `State`

**Responsabilité** : Représenter un état de l'automate.

**Fichier** : `src/baobab_geek_interpreter/lexical/automaton/state.py`

#### Attributs

| Attribut | Type | Description |
|----------|------|-------------|
| `name` | `str` | Nom unique de l'état (ex: "START", "DIGIT") |
| `is_final` | `bool` | Indique si l'état est acceptant |

#### Méthodes

```python
def __init__(self, name: str, is_final: bool = False) -> None:
    """Initialise un état."""

def __eq__(self, other: object) -> bool:
    """Égalité basée sur le nom."""

def __hash__(self) -> int:
    """Hash basé sur le nom (pour utilisation dans des sets/dicts)."""

def __repr__(self) -> str:
    """Représentation pour le débogage."""
```

#### Exemple d'utilisation

```python
start_state = State("START", is_final=False)
digit_state = State("DIGIT", is_final=True)
error_state = State("ERROR", is_final=False)

# Utilisation dans un set
states = {start_state, digit_state, error_state}

# Comparaison
assert start_state != digit_state
```

#### Tests à implémenter

1. ✅ Création d'un état simple
2. ✅ Création d'un état final
3. ✅ Égalité entre états avec même nom
4. ✅ Inégalité entre états avec noms différents
5. ✅ Hash cohérent (même hash pour états égaux)
6. ✅ Utilisation dans un set (pas de doublons)
7. ✅ Utilisation comme clé de dictionnaire
8. ✅ Représentation `__repr__`

---

### 2. Classe `Transition`

**Responsabilité** : Représenter une transition conditionnelle entre deux états.

**Fichier** : `src/baobab_geek_interpreter/lexical/automaton/transition.py`

#### Attributs

| Attribut | Type | Description |
|----------|------|-------------|
| `from_state` | `State` | État source |
| `to_state` | `State` | État destination |
| `condition` | `Callable[[str], bool]` | Fonction qui teste si un caractère active la transition |

#### Méthodes

```python
def __init__(
    self, 
    from_state: State, 
    to_state: State, 
    condition: Callable[[str], bool]
) -> None:
    """Initialise une transition."""

def can_transition(self, char: str) -> bool:
    """Teste si le caractère active la transition.
    
    :param char: Caractère d'entrée (ou chaîne vide pour ε-transition)
    :return: True si la transition est activée
    """

def __repr__(self) -> str:
    """Représentation pour le débogage."""
```

#### Fonctions de condition communes

```python
def is_digit(char: str) -> bool:
    """Vérifie si le caractère est un chiffre (0-9)."""
    return char.isdigit()

def is_letter(char: str) -> bool:
    """Vérifie si le caractère est une lettre (a-z, A-Z)."""
    return char.isalpha()

def is_alpha_numeric(char: str) -> bool:
    """Vérifie si le caractère est alphanumérique."""
    return char.isalnum()

def is_specific(target: str) -> Callable[[str], bool]:
    """Crée une condition pour un caractère spécifique."""
    return lambda char: char == target

def is_in_set(charset: str) -> Callable[[str], bool]:
    """Crée une condition pour un ensemble de caractères."""
    return lambda char: char in charset
```

#### Exemple d'utilisation

```python
start = State("START")
digit = State("DIGIT", is_final=True)

# Transition pour les chiffres
t1 = Transition(start, digit, is_digit)

# Transition pour un caractère spécifique
t2 = Transition(start, digit, is_specific('.'))

# Transition pour un ensemble
t3 = Transition(start, digit, is_in_set('+-'))

# Test
assert t1.can_transition('5') == True
assert t1.can_transition('a') == False
```

#### Tests à implémenter

1. ✅ Création d'une transition simple
2. ✅ `can_transition` retourne True pour condition valide
3. ✅ `can_transition` retourne False pour condition invalide
4. ✅ Transition avec `is_digit`
5. ✅ Transition avec `is_letter`
6. ✅ Transition avec `is_specific`
7. ✅ Transition avec `is_in_set`
8. ✅ Transition avec lambda personnalisée
9. ✅ Gestion des chaînes vides
10. ✅ Représentation `__repr__`

---

### 3. Classe `Automaton`

**Responsabilité** : Moteur principal de l'automate, gère l'exécution.

**Fichier** : `src/baobab_geek_interpreter/lexical/automaton/automaton.py`

#### Attributs

| Attribut | Type | Description |
|----------|------|-------------|
| `states` | `Set[State]` | Ensemble de tous les états |
| `initial_state` | `State` | État de départ |
| `current_state` | `State` | État courant (changé pendant l'exécution) |
| `transitions` | `List[Transition]` | Liste de toutes les transitions |
| `final_states` | `Set[State]` | Ensemble des états acceptants |

#### Méthodes

##### Construction

```python
def __init__(self, initial_state: State) -> None:
    """Initialise un automate avec un état initial.
    
    :param initial_state: État de départ
    """

def add_state(self, state: State) -> None:
    """Ajoute un état à l'automate.
    
    :param state: État à ajouter
    :raises ValueError: Si l'état existe déjà
    """

def add_transition(self, transition: Transition) -> None:
    """Ajoute une transition à l'automate.
    
    :param transition: Transition à ajouter
    :raises ValueError: Si les états source/destination n'existent pas
    """

def set_final_state(self, state: State) -> None:
    """Marque un état comme final.
    
    :param state: État à marquer comme final
    :raises ValueError: Si l'état n'existe pas
    """
```

##### Exécution

```python
def process(self, input_string: str) -> bool:
    """Traite une chaîne d'entrée et retourne si elle est acceptée.
    
    :param input_string: Chaîne à traiter
    :return: True si acceptée (état final atteint), False sinon
    """

def step(self, char: str) -> bool:
    """Exécute un pas de l'automate pour un caractère.
    
    :param char: Caractère d'entrée
    :return: True si transition trouvée, False sinon
    """

def reset(self) -> None:
    """Réinitialise l'automate à l'état initial."""

def is_in_final_state(self) -> bool:
    """Vérifie si l'état courant est final.
    
    :return: True si l'état courant est acceptant
    """

def get_current_state(self) -> State:
    """Retourne l'état courant.
    
    :return: État courant
    """
```

##### Utilitaires

```python
def _find_transition(self, from_state: State, char: str) -> Optional[Transition]:
    """Cherche une transition applicable depuis un état pour un caractère.
    
    :param from_state: État source
    :param char: Caractère d'entrée
    :return: Transition applicable ou None
    """
```

#### Algorithme de `process()`

```python
def process(self, input_string: str) -> bool:
    """Algorithme complet de traitement."""
    self.reset()  # Retour à l'état initial
    
    for char in input_string:
        if not self.step(char):
            return False  # Pas de transition trouvée
    
    return self.is_in_final_state()  # Accepte si état final
```

#### Algorithme de `step()`

```python
def step(self, char: str) -> bool:
    """Exécute un pas de transition."""
    transition = self._find_transition(self.current_state, char)
    
    if transition is None:
        return False  # Échec : pas de transition
    
    self.current_state = transition.to_state  # Changement d'état
    return True
```

#### Exemple d'utilisation : Automate pour entiers positifs

```python
# États
start = State("START", is_final=False)
digit = State("DIGIT", is_final=True)

# Automate
automaton = Automaton(start)
automaton.add_state(start)
automaton.add_state(digit)
automaton.set_final_state(digit)

# Transitions
automaton.add_transition(Transition(start, digit, is_digit))
automaton.add_transition(Transition(digit, digit, is_digit))

# Tests
assert automaton.process("123") == True    # Accepté
assert automaton.process("0") == True      # Accepté
assert automaton.process("abc") == False   # Rejeté
assert automaton.process("") == False      # Rejeté (pas d'état final atteint)
```

#### Tests à implémenter

##### Tests unitaires (`test_automaton.py`)

1. ✅ Création d'un automate simple
2. ✅ Ajout d'états
3. ✅ Ajout de transitions
4. ✅ Définition d'états finaux
5. ✅ `reset()` retourne à l'état initial
6. ✅ `get_current_state()` retourne l'état correct
7. ✅ `is_in_final_state()` détecte correctement
8. ✅ `step()` change d'état correctement
9. ✅ `step()` retourne False si pas de transition
10. ✅ `process()` accepte une chaîne valide
11. ✅ `process()` rejette une chaîne invalide
12. ✅ `process()` sur chaîne vide
13. ✅ Levée d'exception si état inexistant dans transition
14. ✅ Levée d'exception si doublon d'état

##### Tests d'intégration (`test_automaton_integration.py`)

1. ✅ **Automate pour entiers positifs** (`[0-9]+`)
   - Accepte : "0", "123", "999999"
   - Rejette : "", "abc", "12a34"

2. ✅ **Automate pour identifiants** (`[a-zA-Z_][a-zA-Z0-9_]*`)
   - Accepte : "variable", "_private", "CamelCase123"
   - Rejette : "123abc", "", "my-var"

3. ✅ **Automate pour mots-clés spécifiques** (ex: "if")
   - Accepte : "if"
   - Rejette : "IF", "i", "iff", ""

4. ✅ **Automate pour nombres signés** (`-?[0-9]+`)
   - Accepte : "123", "-456", "0"
   - Rejette : "", "--1", "+-1"

5. ✅ **Automate avec choix multiples** (ex: "true" ou "false")
   - Accepte : "true", "false"
   - Rejette : "True", "FALSE", "maybe"

---

## 🎨 Exemples d'Automates Avancés

### Automate pour FLOAT (`-?[0-9]+\.[0-9]+`)

```python
# États
start = State("START")
sign = State("SIGN")
digit_before_dot = State("DIGIT_BEFORE_DOT")
dot = State("DOT")
digit_after_dot = State("DIGIT_AFTER_DOT", is_final=True)

# Construction
automaton = Automaton(start)
for state in [start, sign, digit_before_dot, dot, digit_after_dot]:
    automaton.add_state(state)
automaton.set_final_state(digit_after_dot)

# Transitions
# START -> SIGN (si '-')
automaton.add_transition(Transition(start, sign, is_specific('-')))
# START -> DIGIT_BEFORE_DOT (si chiffre)
automaton.add_transition(Transition(start, digit_before_dot, is_digit))
# SIGN -> DIGIT_BEFORE_DOT (si chiffre)
automaton.add_transition(Transition(sign, digit_before_dot, is_digit))
# DIGIT_BEFORE_DOT -> DIGIT_BEFORE_DOT (si chiffre)
automaton.add_transition(Transition(digit_before_dot, digit_before_dot, is_digit))
# DIGIT_BEFORE_DOT -> DOT (si '.')
automaton.add_transition(Transition(digit_before_dot, dot, is_specific('.')))
# DOT -> DIGIT_AFTER_DOT (si chiffre)
automaton.add_transition(Transition(dot, digit_after_dot, is_digit))
# DIGIT_AFTER_DOT -> DIGIT_AFTER_DOT (si chiffre)
automaton.add_transition(Transition(digit_after_dot, digit_after_dot, is_digit))

# Tests
assert automaton.process("3.14") == True
assert automaton.process("-0.5") == True
assert automaton.process("123.456789") == True
assert automaton.process("3.") == False      # Pas de chiffre après '.'
assert automaton.process(".14") == False     # Pas de chiffre avant '.'
assert automaton.process("--1.0") == False   # Double signe
```

### Automate pour STRING (simplifié)

**Note** : Les chaînes avec échappement sont complexes. Voici une version simplifiée pour `"[a-zA-Z]*"`.

```python
# États
start = State("START")
opening_quote = State("OPENING_QUOTE")
content = State("CONTENT")
closing_quote = State("CLOSING_QUOTE", is_final=True)

# Construction
automaton = Automaton(start)
for state in [start, opening_quote, content, closing_quote]:
    automaton.add_state(state)
automaton.set_final_state(closing_quote)

# Transitions
automaton.add_transition(Transition(start, opening_quote, is_specific('"')))
automaton.add_transition(Transition(opening_quote, content, is_letter))
automaton.add_transition(Transition(opening_quote, closing_quote, is_specific('"')))  # Chaîne vide
automaton.add_transition(Transition(content, content, is_letter))
automaton.add_transition(Transition(content, closing_quote, is_specific('"')))

# Tests
assert automaton.process('""') == True           # Chaîne vide
assert automaton.process('"hello"') == True
assert automaton.process('"world"') == True
assert automaton.process('"') == False           # Pas de fermeture
assert automaton.process('"test') == False       # Pas de fermeture
assert automaton.process('hello"') == False      # Pas d'ouverture
```

**Note importante** : Pour gérer les séquences d'échappement (`\"`, `\\`, `\n`, `\t`), l'automate sera plus complexe. Cela sera implémenté dans la Phase 4 (Analyseur Lexical) avec des fonctions spécifiques.

---

## 🧪 Stratégie de Tests

### Tests Unitaires

**Fichiers** : `test_state.py`, `test_transition.py`, `test_automaton.py`

**Couverture** :
- Toutes les méthodes publiques
- Cas normaux et cas limites
- Gestion d'erreurs (exceptions)
- Égalité et hashage pour `State`

### Tests d'Intégration

**Fichier** : `test_automaton_integration.py`

**Objectif** : Valider des automates complets et réalistes

**Exemples** :
1. Automate pour entiers
2. Automate pour identifiants
3. Automate pour mots-clés
4. Automate pour nombres signés
5. Automate avec branches multiples

### Benchmarks de Performance (optionnel)

**Objectif** : Mesurer les performances sur des entrées longues

**Exemple** :
```python
def test_performance_long_input():
    """Teste les performances sur une entrée longue."""
    automaton = create_integer_automaton()
    long_input = "1234567890" * 1000  # 10,000 chiffres
    
    import time
    start = time.time()
    result = automaton.process(long_input)
    duration = time.time() - start
    
    assert result == True
    assert duration < 0.1  # Moins de 100ms
```

---

## ✅ Critères de Validation

### Fonctionnels

- [ ] Un automate peut reconnaître un motif simple (ex: `[0-9]+`)
- [ ] Un automate peut reconnaître un motif complexe (ex: `-?[0-9]+\.[0-9]+`)
- [ ] Les transitions sont correctement évaluées
- [ ] Les états finaux sont correctement détectés
- [ ] La méthode `reset()` réinitialise l'automate
- [ ] Les erreurs (états inexistants, etc.) lèvent des exceptions

### Qualité

- [ ] **Tests unitaires** : Tous les tests passent
- [ ] **Couverture** : ≥ 90% de couverture de code
- [ ] **Black** : Code formaté sans erreur
- [ ] **Pylint** : Score ≥ 9.5/10
- [ ] **Mypy** : Aucune erreur de typage
- [ ] **Flake8** : Aucune violation PEP 8
- [ ] **Bandit** : Aucune vulnérabilité de sécurité

### Documentation

- [ ] Docstrings complètes (reStructuredText)
- [ ] Exemples d'utilisation dans les docstrings
- [ ] Types annotés pour tous les paramètres et retours

---

## 🚀 Plan d'Exécution

### Étape 1 : Créer `State` (30 min)
1. Créer le fichier `src/baobab_geek_interpreter/lexical/automaton/state.py`
2. Implémenter la classe `State`
3. Créer le fichier de tests `tests/test_baobab_geek_interpreter/lexical/automaton/test_state.py`
4. Exécuter les tests
5. Vérifier la qualité du code

### Étape 2 : Créer `Transition` (30 min)
1. Créer le fichier `src/baobab_geek_interpreter/lexical/automaton/transition.py`
2. Implémenter la classe `Transition`
3. Implémenter les fonctions de condition (`is_digit`, `is_letter`, etc.)
4. Créer le fichier de tests `tests/test_baobab_geek_interpreter/lexical/automaton/test_transition.py`
5. Exécuter les tests
6. Vérifier la qualité du code

### Étape 3 : Créer `Automaton` (2 heures)
1. Créer le fichier `src/baobab_geek_interpreter/lexical/automaton/automaton.py`
2. Implémenter la classe `Automaton`
3. Créer le fichier de tests `tests/test_baobab_geek_interpreter/lexical/automaton/test_automaton.py`
4. Exécuter les tests
5. Vérifier la qualité du code

### Étape 4 : Tests d'Intégration (1 heure)
1. Créer le fichier `tests/test_baobab_geek_interpreter/lexical/automaton/test_automaton_integration.py`
2. Implémenter les automates de test (entiers, identifiants, etc.)
3. Exécuter les tests d'intégration
4. Vérifier la couverture globale

### Étape 5 : Finalisation (30 min)
1. Mettre à jour `src/baobab_geek_interpreter/lexical/automaton/__init__.py`
2. Exporter les classes principales
3. Mettre à jour le journal de développement (`docs/dev_diary.md`)
4. Commit et push

---

## 🔧 Dépendances

### Imports Python Standard

```python
from abc import ABC, abstractmethod
from typing import Any, Callable, List, Optional, Set
```

### Dépendances Internes

Aucune. Cette phase est **autonome** et ne dépend d'aucune autre classe du projet.

---

## 📊 Métriques Attendues

| Métrique | Valeur Cible |
|----------|--------------|
| Lignes de code (LOC) | ~200-250 |
| Nombre de tests | ~40-50 |
| Couverture de code | ≥ 90% |
| Score Pylint | ≥ 9.5/10 |
| Temps d'exécution tests | < 1 seconde |
| Performance (10K chars) | < 100ms |

---

## 🎓 Références Théoriques

- **Théorie des automates** : Hopcroft, Motwani, Ullman - "Introduction to Automata Theory, Languages, and Computation"
- **Compilateurs** : Aho, Lam, Sethi, Ullman - "Compilers: Principles, Techniques, and Tools" (Dragon Book)
- **Expressions régulières** : Les automates implémentés correspondent aux expressions régulières suivantes :
  - Entiers : `[0-9]+`
  - Identifiants : `[a-zA-Z_][a-zA-Z0-9_]*`
  - Flottants : `-?[0-9]+\.[0-9]+`

---

## 🔮 Évolutions Futures (hors scope Phase 3)

- **Automates Non-Déterministes (AFN)** : Permettraient des constructions plus simples
- **Epsilon-transitions** : Transitions sans consommer de caractère
- **Minimisation d'automate** : Réduction du nombre d'états
- **Compilation d'expressions régulières** : Génération automatique d'automates depuis regex
- **Optimisations** : Tables de transitions pré-calculées pour plus de performance

Ces améliorations pourront être envisagées dans les versions futures (v1.1+).

---

## 📝 Résumé

La Phase 3 pose les **fondations algorithmiques** de l'interpréteur en créant un moteur d'automates robuste et générique. Ce moteur sera ensuite utilisé dans la Phase 4 pour implémenter l'analyseur lexical complet.

**Livrables** :
- ✅ Classe `State` complète et testée
- ✅ Classe `Transition` complète et testée
- ✅ Classe `Automaton` complète et testée
- ✅ Tests d'intégration avec automates réalistes
- ✅ Documentation complète
- ✅ Qualité de code validée

Une fois cette phase terminée, nous disposerons d'un outil puissant et réutilisable pour reconnaître n'importe quel motif dans le code source du langage "geek".
