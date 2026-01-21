# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [1.0.0] - 2026-01-22

### 🎉 Version initiale

Première version stable de Baobab Geek Interpreter.

### Ajouté

#### Core Features
- **Interpréteur complet** pour le langage "geek"
- **Pipeline d'analyse** : lexical → syntaxique → sémantique → exécution
- **Classe `Interpreter`** : interface unifiée pour l'utilisateur
- **Décorateur `@service`** : marquage simple des fonctions interprétables
- **Enregistrement automatique** : découverte des services dans un module

#### Types supportés
- **Types primitifs** : `int`, `float`, `str`
- **Tableaux homogènes** : `list[int]`, `list[float]`, `list[str]`
- **Validation stricte** : pas de conversion automatique

#### Analyseur Lexical
- **Tokenisation complète** : identifiants, nombres, chaînes, délimiteurs
- **Support des nombres négatifs** : `-42`, `-3.14`
- **Échappement dans les chaînes** : `\"`, `\\`, `\n`, `\t`
- **Moteur DFA générique** : `State`, `Transition`, `Automaton`

#### Analyseur Syntaxique
- **Parser descendant récursif** : LL(1)
- **Construction d'AST** : arbre syntaxique abstrait
- **Pattern Visitor** : pour le parcours de l'AST
- **Nœuds AST** : `ServiceCallNode`, `ArgumentNode`, `IntNode`, `FloatNode`, `StringNode`, `ArrayNode`

#### Analyseur Sémantique
- **Validation des services** : existence dans la table des symboles
- **Vérification des types** : compatibilité stricte avec la signature
- **Validation des tableaux** : homogénéité et absence d'imbrication (v1.0)
- **TypeChecker** : vérification avancée avec support des types génériques

#### Exécuteur
- **Pattern Visitor** : implémentation complète pour l'exécution
- **Appel de services** : avec arguments évalués récursivement
- **Gestion d'erreurs** : encapsulation dans `BaobabExecutionException`
- **Support tous types de retour** : `int`, `float`, `str`, `list`, `None`

#### Gestion des Exceptions
- **Hiérarchie complète** :
  - `BaobabGeekInterpreterException` : base
  - `BaobabLexicalAnalyserException` : erreurs lexicales
  - `BaobabSyntaxAnalyserException` : erreurs syntaxiques
  - `BaobabSemanticAnalyserException` : erreurs sémantiques
  - `BaobabExecutionException` : erreurs d'exécution
- **Contexte détaillé** : position, ligne, colonne, source
- **Exception originale** : préservée dans `BaobabExecutionException`

#### API Publique
- **`Interpreter`** : classe principale
- **`service`** : décorateur
- **Exceptions** : toutes exportées
- **Documentation** : docstrings complètes partout

#### Tests
- **516 tests** : unitaires et d'intégration
- **Couverture élevée** : >90% sur les modules principaux
- **100% sur modules clés** : `Interpreter`, `Executor`, `SemanticAnalyzer`
- **Tests bout-en-bout** : scénarios réels complets

#### Qualité
- **Pylint** : 10.00/10
- **MyPy** : aucune erreur de typage
- **Flake8** : conformité PEP 8 complète
- **Bandit** : aucun problème de sécurité
- **Black** : formatage uniforme

#### Documentation
- **README.md** : documentation complète
- **CHANGELOG.md** : historique des versions
- **Exemples** : cas d'usage variés
- **Docstrings** : toutes les fonctions publiques
- **Type hints** : annotations complètes

### Contraintes et Limitations (v1.0)

- **Tableaux imbriqués** : non supportés dans cette version
- **Types personnalisés** : uniquement types primitifs et tableaux
- **Conversion automatique** : aucune (validation stricte)
- **Contexte d'exécution** : pas de variables ou d'état partagé
- **Appels imbriqués** : pas de composition de services

### Notes techniques

#### Architecture
- **Modular** : composants indépendants et testables
- **Extensible** : facile d'ajouter de nouveaux types ou fonctionnalités
- **Performant** : DFA optimisé pour l'analyse lexicale
- **Robuste** : gestion d'erreurs à chaque phase

#### Dépendances
- **Python** : 3.10+
- **Aucune dépendance externe** : bibliothèque standard uniquement
- **Dev dependencies** : pytest, pytest-cov, black, pylint, mypy, flake8, bandit

#### Workflow de développement
- **Git flow** : branches feature, pull requests, review
- **Conventional commits** : messages de commit structurés
- **CI/CD** : tests automatiques, quality checks
- **Documentation** : mise à jour continue

### Remerciements

Merci à tous les contributeurs qui ont rendu cette première version possible !

---

## [Unreleased]

### Prévu pour v1.1
- Optimisation des performances
- Documentation interactive
- Amélioration des messages d'erreur

### Prévu pour v2.0
- Support des tableaux imbriqués
- Types personnalisés
- Composition de services
- Variables et contexte d'exécution

---

**Légende** :
- `Ajouté` : nouvelles fonctionnalités
- `Modifié` : changements dans les fonctionnalités existantes
- `Déprécié` : fonctionnalités bientôt supprimées
- `Supprimé` : fonctionnalités retirées
- `Corrigé` : corrections de bugs
- `Sécurité` : corrections de vulnérabilités

[1.0.0]: https://github.com/baobabgit/baobab_geek_interpreter/releases/tag/v1.0.0
[Unreleased]: https://github.com/baobabgit/baobab_geek_interpreter/compare/v1.0.0...HEAD
