# Phases de Développement - Baobab Geek Interpreter v1.0

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Planning général](#planning-général)
3. [Phases détaillées](#phases-détaillées)
4. [Dépendances entre phases](#dépendances-entre-phases)
5. [Critères de validation](#critères-de-validation)
6. [Livrables](#livrables)

---

## Vue d'ensemble

Le développement du Baobab Geek Interpreter est organisé en **10 phases** progressives, chacune construisant sur les fondations de la précédente. L'approche privilégie la construction incrémentale avec validation par tests unitaires à chaque étape.

### Durée estimée
- **Total** : ~15 jours de développement
- **Par phase** : 1-2 jours en moyenne
- **Tests** : Intégrés dans chaque phase

### Méthodologie
- Développement piloté par les tests (TDD)
- Couverture de code minimum : 90%
- Validation par tous les outils de qualité (black, pylint, mypy, flake8, bandit)
- Documentation continue dans `dev_diary.md`

---

## Planning général

| Phase | Nom | Durée | Effort | Priorité |
|-------|-----|-------|--------|----------|
| 1 | Exceptions | 1-2h | ⚡ Faible | 🔴 Critique |
| 2 | Types de base | 2-3h | ⚡ Faible | 🔴 Critique |
| 3 | Automate | 1 jour | ⚡⚡ Moyen | 🔴 Critique |
| 4 | Analyseur Lexical | 2 jours | ⚡⚡⚡ Fort | 🔴 Critique |
| 5 | Analyseur Syntaxique | 2 jours | ⚡⚡⚡ Fort | 🔴 Critique |
| 6 | Table des symboles | 1 jour | ⚡⚡ Moyen | 🟡 Haute |
| 7 | Analyseur Sémantique | 2 jours | ⚡⚡⚡ Fort | 🟡 Haute |
| 8 | Exécuteur | 2 jours | ⚡⚡⚡ Fort | 🟡 Haute |
| 9 | Intégration | 1 jour | ⚡⚡ Moyen | 🟢 Normale |
| 10 | Documentation | 1 jour | ⚡⚡ Moyen | 🟢 Normale |

---

## Phases détaillées

### Phase 1 : Hiérarchie d'exceptions

**Durée** : 1-2 heures  
**Objectif** : Créer toutes les classes d'exceptions personnalisées du projet.

#### Fichiers à créer

```
src/baobab_geek_interpreter/exceptions/
├── __init__.py
├── base_exception.py
├── lexical_exception.py
├── syntax_exception.py
├── semantic_exception.py
└── execution_exception.py

tests/baobab_geek_interpreter/exceptions/
├── __init__.py
├── test_base_exception.py
├── test_lexical_exception.py
├── test_syntax_exception.py
├── test_semantic_exception.py
└── test_execution_exception.py
```

#### Tâches

1. ✅ Créer `BaobabGeekInterpreterException` avec attributs contextuels
   - `message`, `source`, `position`, `line`, `column`
   - Méthode `__str__` formatée
2. ✅ Créer `BaobabLexicalAnalyserException`
3. ✅ Créer `BaobabSyntaxAnalyserException`
4. ✅ Créer `BaobabSemanticAnalyserException`
5. ✅ Créer `BaobabExecutionException` avec attributs spécifiques
   - `service_name`, `original_exception`
6. ✅ Tests unitaires pour toutes les exceptions
7. ✅ Vérifier couverture ≥ 90%

#### Critères de validation

- [ ] Toutes les exceptions héritent de `BaobabGeekInterpreterException`
- [ ] Tous les attributs sont correctement typés
- [ ] Tests unitaires passent (pytest)
- [ ] Couverture ≥ 90%
- [ ] Pas d'erreur pylint, mypy, flake8
- [ ] Documentation (docstrings) complète

#### Livrable

- Hiérarchie d'exceptions complète et testée
- Prête à être utilisée par tous les autres modules

---

### Phase 2 : Types de base

**Durée** : 2-3 heures  
**Objectif** : Définir les énumérations et structures de données fondamentales.

#### Fichiers à créer

```
src/baobab_geek_interpreter/lexical/
├── __init__.py
├── token_type.py
└── token.py

src/baobab_geek_interpreter/syntax/
├── __init__.py
└── ast_node.py

tests/baobab_geek_interpreter/lexical/
├── test_token_type.py
└── test_token.py

tests/baobab_geek_interpreter/syntax/
└── test_ast_node.py
```

#### Tâches

1. ✅ Créer `TokenType` (enum)
   - INT, FLOAT, STRING, IDENTIFIANT
   - LPAREN, RPAREN, LBRACKET, RBRACKET, COMMA
   - EOF
2. ✅ Créer `Token` (dataclass ou classe)
   - Attributs : type, value, position, line, column
3. ✅ Créer hiérarchie de classes AST
   - `ASTNode` (base abstraite)
   - `ServiceCallNode`
   - `ArgumentNode`
   - `ConstantNode` (base abstraite)
   - `IntNode`, `FloatNode`, `StringNode`, `ArrayNode`
4. ✅ Implémenter le pattern Visitor
   - `ASTVisitor` (interface abstraite)
   - Méthode `accept()` dans chaque nœud
5. ✅ Tests unitaires
6. ✅ Documentation

#### Critères de validation

- [ ] Tous les types sont définis et typés
- [ ] Pattern Visitor correctement implémenté
- [ ] Tests unitaires passent
- [ ] Couverture ≥ 90%
- [ ] Pas d'erreur des outils de qualité

#### Livrable

- Structures de données prêtes pour l'analyse lexicale et syntaxique

---

### Phase 3 : Automate fini déterministe

**Durée** : 1 jour  
**Objectif** : Implémenter le moteur d'automate pour l'analyse lexicale.

#### Fichiers à créer

```
src/baobab_geek_interpreter/lexical/automaton/
├── __init__.py
├── state.py
├── transition.py
└── automaton.py

tests/baobab_geek_interpreter/lexical/automaton/
├── test_state.py
├── test_transition.py
├── test_automaton.py
└── test_automaton_integration.py
```

#### Tâches

1. ✅ Créer classe `State`
   - Attributs : name, is_final
   - Méthodes : `__eq__`, `__hash__`, `__repr__`
2. ✅ Créer classe `Transition`
   - Attributs : from_state, to_state, condition (Callable)
   - Méthode : `can_transition(char: str) -> bool`
3. ✅ Créer classe `Automaton`
   - Attributs : states, initial_state, transitions, final_states
   - Méthodes :
     - `add_state(state: State)`
     - `add_transition(transition: Transition)`
     - `process(input: str) -> bool`
     - `get_current_state() -> State`
     - `reset()`
4. ✅ Tests unitaires détaillés
   - Tests d'automate simple (accepte "ab")
   - Tests d'automate complexe (nombres, identifiants)
5. ✅ Tests d'intégration

#### Critères de validation

- [ ] Automate reconnaît correctement les motifs
- [ ] Gestion des états finaux et non-finaux
- [ ] Tests unitaires exhaustifs
- [ ] Couverture ≥ 90%
- [ ] Performance acceptable (benchmark simple)

#### Livrable

- Moteur d'automate générique et réutilisable

---

### Phase 4 : Analyseur Lexical

**Durée** : 2 jours  
**Objectif** : Transformer une chaîne source en liste de tokens.

#### Fichiers à créer

```
src/baobab_geek_interpreter/lexical/
└── lexical_analyzer.py

tests/baobab_geek_interpreter/lexical/
├── test_lexical_analyzer.py
└── test_lexical_analyzer_integration.py
```

#### Tâches

1. ✅ Créer automate pour INT (`-?[0-9]+`)
2. ✅ Créer automate pour FLOAT (`-?[0-9]+\.[0-9]+`)
3. ✅ Créer automate pour STRING (`"([^"\\]|\\.)*"`)
   - Gestion de l'échappement : `\"`, `\\`, `\n`, `\t`
4. ✅ Créer automate pour IDENTIFIANT (`[a-zA-Z_][a-zA-Z0-9_]*`)
5. ✅ Créer classe `LexicalAnalyzer`
   - Méthode : `analyze(source: str) -> List[Token]`
   - Gestion des délimiteurs : `(`, `)`, `[`, `]`, `,`
   - Élimination des espaces non significatifs
   - Détection et rapport d'erreurs
6. ✅ Tests exhaustifs
   - Tokens individuels
   - Combinaisons de tokens
   - Gestion des erreurs
   - Cas limites (string vide, nombres négatifs, etc.)
7. ✅ Benchmarks de performance

#### Critères de validation

- [ ] Tous les types de tokens sont reconnus
- [ ] Échappement des strings fonctionne
- [ ] Nombres négatifs correctement traités
- [ ] Espaces ignorés sauf dans les strings
- [ ] Erreurs lexicales détectées avec position précise
- [ ] Tests unitaires complets
- [ ] Couverture ≥ 90%

#### Livrable

- Analyseur lexical complet et robuste

---

### Phase 5 : Analyseur Syntaxique

**Durée** : 2 jours  
**Objectif** : Construire un AST à partir de la liste de tokens.

#### Fichiers à créer

```
src/baobab_geek_interpreter/syntax/
└── syntax_analyzer.py

tests/baobab_geek_interpreter/syntax/
├── test_syntax_analyzer.py
└── test_syntax_analyzer_integration.py
```

#### Tâches

1. ✅ Créer classe `SyntaxAnalyzer`
   - Parser descendant récursif
   - Une méthode par règle de grammaire :
     - `parse_appel_service() -> ServiceCallNode`
     - `parse_liste_arguments() -> List[ArgumentNode]`
     - `parse_argument() -> ArgumentNode`
     - `parse_constante() -> ConstantNode`
     - `parse_tableau() -> ArrayNode`
2. ✅ Gestion des erreurs syntaxiques
   - Token inattendu
   - Parenthèse/crochet non fermé
   - Position précise de l'erreur
3. ✅ Tests exhaustifs
   - Appels simples : `service()`
   - Appels avec arguments : `service(1, 2, "test")`
   - Appels avec tableaux : `service([1, 2, 3])`
   - Erreurs syntaxiques variées
4. ✅ Validation de l'AST généré

#### Critères de validation

- [ ] AST correctement construit pour tous les cas valides
- [ ] Erreurs syntaxiques détectées avec précision
- [ ] Messages d'erreur clairs et informatifs
- [ ] Tests unitaires complets
- [ ] Couverture ≥ 90%

#### Livrable

- Analyseur syntaxique complet avec construction d'AST

---

### Phase 6 : Table des symboles et décorateur

**Durée** : 1 jour  
**Objectif** : Gérer l'enregistrement et la recherche des services.

#### Fichiers à créer

```
src/baobab_geek_interpreter/semantic/
├── __init__.py
└── symbol_table.py

src/baobab_geek_interpreter/execution/
├── __init__.py
└── service_decorator.py

tests/baobab_geek_interpreter/semantic/
└── test_symbol_table.py

tests/baobab_geek_interpreter/execution/
└── test_service_decorator.py
```

#### Tâches

1. ✅ Créer décorateur `@service`
   - Marque les fonctions avec `_is_service = True`
   - Ajoute métadonnée `_service_name`
2. ✅ Créer classe `SymbolTable`
   - Méthodes :
     - `register(name: str, func: Callable)`
     - `get(name: str) -> Callable | None`
     - `has(name: str) -> bool`
     - `discover_services(module: Any)`
     - `list_services() -> List[str]`
3. ✅ Tests
   - Enregistrement manuel
   - Découverte automatique
   - Recherche de services
   - Gestion des doublons

#### Critères de validation

- [ ] Décorateur fonctionne correctement
- [ ] Découverte automatique des services
- [ ] Table des symboles thread-safe (optionnel v1.0)
- [ ] Tests unitaires complets
- [ ] Couverture ≥ 90%

#### Livrable

- Système de gestion des services fonctionnel

---

### Phase 7 : Analyseur Sémantique

**Durée** : 2 jours  
**Objectif** : Valider l'AST avant l'exécution.

#### Fichiers à créer

```
src/baobab_geek_interpreter/semantic/
├── type_checker.py
└── semantic_analyzer.py

tests/baobab_geek_interpreter/semantic/
├── test_type_checker.py
├── test_semantic_analyzer.py
└── test_semantic_analyzer_integration.py
```

#### Tâches

1. ✅ Créer classe `TypeChecker`
   - Méthode : `check_types(signature, args) -> bool`
   - Validation stricte (pas de conversion auto)
   - Support des types : int, float, str, list[T]
2. ✅ Créer classe `SemanticAnalyzer`
   - Méthode : `analyze(ast: ASTNode)`
   - Vérifications :
     - Service existe dans la table des symboles
     - Nombre d'arguments correct
     - Types d'arguments compatibles
     - Tableaux homogènes
     - Pas de tableaux imbriqués (v1.0)
3. ✅ Tests exhaustifs
   - Service inexistant
   - Mauvais nombre d'arguments
   - Types incompatibles
   - Tableaux hétérogènes
   - Tableaux imbriqués (doit échouer)

#### Critères de validation

- [ ] Toutes les règles sémantiques vérifiées
- [ ] Messages d'erreur précis et utiles
- [ ] Tests unitaires complets
- [ ] Couverture ≥ 90%

#### Livrable

- Analyseur sémantique avec validation stricte

---

### Phase 8 : Exécuteur

**Durée** : 2 jours  
**Objectif** : Exécuter l'AST et retourner le résultat.

#### Fichiers à créer

```
src/baobab_geek_interpreter/execution/
└── executor.py

tests/baobab_geek_interpreter/execution/
├── test_executor.py
└── test_executor_integration.py
```

#### Tâches

1. ✅ Créer classe `Executor` implémentant `ASTVisitor`
   - Méthode : `execute(ast: ASTNode) -> Any`
   - Implémentation de toutes les méthodes visit_*
   - `visit_service_call()` : Appel du service
   - `visit_int/float/string()` : Conversion des valeurs
   - `visit_array()` : Construction de liste Python
2. ✅ Gestion des exceptions
   - Wrapper des exceptions des services
   - `BaobabExecutionException` avec contexte
3. ✅ Tests exhaustifs
   - Exécution de services simples
   - Exécution avec différents types d'arguments
   - Gestion des exceptions
   - Valeurs de retour variées

#### Critères de validation

- [ ] Tous les types de nœuds AST sont visités
- [ ] Services exécutés correctement
- [ ] Exceptions encapsulées proprement
- [ ] Tests unitaires complets
- [ ] Couverture ≥ 90%

#### Livrable

- Exécuteur fonctionnel avec gestion d'erreurs robuste

---

### Phase 9 : Intégration

**Durée** : 1 jour  
**Objectif** : Assembler tous les composants dans l'interface principale.

#### Fichiers à créer

```
src/baobab_geek_interpreter/
├── __init__.py
└── interpreter.py

tests/baobab_geek_interpreter/
├── test_interpreter.py
└── integration/
    ├── __init__.py
    └── test_full_interpreter.py
```

#### Tâches

1. ✅ Créer classe `Interpreter`
   - Initialisation de tous les composants
   - Méthode : `interpret(source: str) -> Any`
   - Méthode : `register_services(module: Any)`
   - Pipeline complet : lexical → syntax → semantic → execution
2. ✅ Configurer `__init__.py` pour exports publics
   - `Interpreter`
   - `service` (décorateur)
   - Exceptions principales
3. ✅ Tests d'intégration bout-en-bout
   - Scénarios réels d'utilisation
   - Tous les types d'arguments
   - Toutes les erreurs possibles
4. ✅ Tests de performance
   - Benchmark sur appels simples
   - Benchmark sur tableaux larges

#### Critères de validation

- [ ] Pipeline complet fonctionne
- [ ] Tous les exemples du cahier des charges fonctionnent
- [ ] Tests d'intégration passent
- [ ] Couverture globale ≥ 90%
- [ ] Performance acceptable

#### Livrable

- Bibliothèque complète et fonctionnelle

---

### Phase 10 : Documentation et exemples

**Durée** : 1 jour  
**Objectif** : Finaliser la documentation utilisateur et les exemples.

#### Fichiers à créer

```
README.md
CHANGELOG.md
examples/
├── basic_usage.py
├── advanced_usage.py
├── error_handling.py
└── custom_services.py
docs/
├── api_reference.md (optionnel)
└── tutorial.md (optionnel)
```

#### Tâches

1. ✅ Créer `README.md` complet
   - Description du projet
   - Installation
   - Quick start
   - Exemples d'utilisation
   - Documentation de l'API
   - Contribution
   - Licence
2. ✅ Créer `CHANGELOG.md`
   - Version 1.0.0 avec toutes les fonctionnalités
3. ✅ Créer exemples dans `examples/`
   - Usage basique
   - Tableaux
   - Gestion d'erreurs
   - Services personnalisés
4. ✅ Mettre à jour `dev_diary.md`
   - Récapitulatif complet du développement
5. ✅ Documentation API (optionnel)
   - Génération avec Sphinx ou MkDocs
   - Hébergement sur Read the Docs

#### Critères de validation

- [ ] README clair et complet
- [ ] Exemples fonctionnels et pédagogiques
- [ ] CHANGELOG à jour
- [ ] Documentation API accessible (si générée)

#### Livrable

- Documentation complète prête pour la release v1.0.0

---

## Dépendances entre phases

```
Phase 1 (Exceptions)
    ↓
Phase 2 (Types de base)
    ↓
Phase 3 (Automate)
    ↓
Phase 4 (Analyseur Lexical)
    ↓
Phase 5 (Analyseur Syntaxique)
    ↓
Phase 6 (Table des symboles) ──┐
    ↓                           │
Phase 7 (Analyseur Sémantique)←┘
    ↓
Phase 8 (Exécuteur) ←──────────┘
    ↓
Phase 9 (Intégration)
    ↓
Phase 10 (Documentation)
```

### Contraintes de dépendances

- **Phases 1-2** : Peuvent être développées en parallèle
- **Phase 3** : Dépend de la phase 1 (exceptions)
- **Phase 4** : Dépend strictement de la phase 3 (automate)
- **Phase 6** : Peut être développée en parallèle de la phase 5
- **Phase 7** : Dépend des phases 5 et 6
- **Phase 8** : Dépend de toutes les phases précédentes
- **Phases 9-10** : Doivent être séquentielles

---

## Critères de validation globaux

### Pour chaque phase

- [ ] Tous les tests unitaires passent
- [ ] Couverture de code ≥ 90%
- [ ] Pas d'erreur black (formatage)
- [ ] Pas d'erreur pylint (linting)
- [ ] Pas d'erreur mypy (types)
- [ ] Pas d'erreur flake8 (style)
- [ ] Pas d'alerte bandit (sécurité)
- [ ] Documentation (docstrings) complète
- [ ] Entry dans `dev_diary.md`
- [ ] Commit avec message Conventional Commits

### Pour la release v1.0.0

- [ ] Toutes les phases complétées
- [ ] Couverture globale ≥ 90%
- [ ] README.md complet
- [ ] CHANGELOG.md à jour
- [ ] Exemples fonctionnels
- [ ] Tag Git `v1.0.0`
- [ ] Package publié sur PyPI (optionnel)

---

## Livrables

### Livrable final v1.0.0

```
baobab-geek-interpreter/
├── src/baobab_geek_interpreter/      # Code source complet
├── tests/                             # Tests exhaustifs
├── docs/                              # Documentation technique
├── examples/                          # Exemples d'utilisation
├── README.md                          # Documentation utilisateur
├── CHANGELOG.md                       # Historique des versions
├── pyproject.toml                     # Configuration complète
├── .gitignore                         # Fichiers ignorés
└── LICENSE                            # Licence du projet
```

### Métriques attendues

- **Lignes de code** : ~2000-3000 lignes (src)
- **Lignes de tests** : ~3000-4000 lignes (tests)
- **Couverture** : ≥ 90%
- **Nombre de classes** : ~25-30 classes
- **Nombre de fichiers** : ~40-50 fichiers
- **Performance** : < 10ms pour analyse simple

---

## Suivi de progression

### Template pour `dev_diary.md`

Après chaque phase, ajouter une entrée :

```markdown
## YYYY-MM-DD HH:MM:SS

### Modifications
- [Phase X] Implémentation de ...
- Création des fichiers : ...
- Tests unitaires : ...

### Buts
- Objectif de la phase
- Ce que cela apporte au projet

### Impact
- État d'avancement global
- Fonctionnalités disponibles
- Prochaines étapes
```

### Commande de vérification

```bash
# Exécuter tous les checks qualité
pytest --cov=src --cov-report=term-missing
black src/ tests/
pylint src/
mypy src/
flake8 src/
bandit -r src/
```

---

## Remarques

- **Flexibilité** : Les durées sont indicatives et peuvent varier
- **Itération** : Retours en arrière possibles si problèmes détectés
- **Documentation continue** : Ne pas attendre la phase 10 pour documenter
- **Tests first** : Privilégier le TDD quand possible
- **Revue de code** : Vérifier systématiquement la qualité avant de passer à la phase suivante

---

**Mise à jour** : 2026-01-21  
**Version** : 1.0  
**Statut** : Prêt pour démarrage du développement
