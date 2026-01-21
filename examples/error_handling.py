"""Exemple de gestion des erreurs avec Baobab Geek Interpreter."""

from baobab_geek_interpreter import (
    Interpreter,
    service,
    BaobabLexicalAnalyserException,
    BaobabSyntaxAnalyserException,
    BaobabSemanticAnalyserException,
    BaobabExecutionException,
)


def main() -> None:
    """Démonstration de la gestion des erreurs."""
    print("=" * 60)
    print("Baobab Geek Interpreter - Gestion des Erreurs")
    print("=" * 60)
    print()

    interpreter = Interpreter()

    # Définir quelques services
    @service
    def add(a: int, b: int) -> int:
        return a + b

    @service
    def divide(a: int, b: int) -> float:
        return a / b

    @service
    def validate_age(age: int) -> str:
        if age < 0:
            raise ValueError("L'âge ne peut pas être négatif")
        if age < 18:
            return "Mineur"
        return "Majeur"

    interpreter.register_service("add", add)
    interpreter.register_service("divide", divide)
    interpreter.register_service("validate_age", validate_age)

    # 1. Erreur lexicale
    print("1. Erreur lexicale (caractère invalide)")
    try:
        interpreter.interpret("add(10, @)")
    except BaobabLexicalAnalyserException as e:
        print(f"   ❌ {type(e).__name__}: {e}")
    print()

    # 2. Erreur syntaxique
    print("2. Erreur syntaxique (parenthèse manquante)")
    try:
        interpreter.interpret("add(10, 20")
    except BaobabSyntaxAnalyserException as e:
        print(f"   ❌ {type(e).__name__}: {e}")
    print()

    # 3. Erreur sémantique - service inconnu
    print("3. Erreur sémantique (service inconnu)")
    try:
        interpreter.interpret("unknown_service(42)")
    except BaobabSemanticAnalyserException as e:
        print(f"   ❌ {type(e).__name__}: {e}")
    print()

    # 4. Erreur sémantique - types incompatibles
    print("4. Erreur sémantique (types incompatibles)")
    try:
        interpreter.interpret('add(10, "20")')
    except BaobabSemanticAnalyserException as e:
        print(f"   ❌ {type(e).__name__}: {e}")
    print()

    # 5. Erreur sémantique - mauvais nombre d'arguments
    print("5. Erreur sémantique (mauvais nombre d'arguments)")
    try:
        interpreter.interpret("add(10)")
    except BaobabSemanticAnalyserException as e:
        print(f"   ❌ {type(e).__name__}: {e}")
    print()

    # 6. Erreur sémantique - tableau hétérogène
    print("6. Erreur sémantique (tableau hétérogène)")

    @service
    def process(numbers: list[int]) -> int:
        return sum(numbers)

    interpreter.register_service("process", process)

    try:
        interpreter.interpret("process([1, 2.5, 3])")
    except BaobabSemanticAnalyserException as e:
        print(f"   ❌ {type(e).__name__}: {e}")
    print()

    # 7. Erreur d'exécution - division par zéro
    print("7. Erreur d'exécution (division par zéro)")
    try:
        interpreter.interpret("divide(10, 0)")
    except BaobabExecutionException as e:
        print(f"   ❌ {type(e).__name__}: {e}")
        print(f"   Service: {e.service_name}")
        print(f"   Exception originale: {type(e.original_exception).__name__}")
    print()

    # 8. Erreur d'exécution - exception personnalisée
    print("8. Erreur d'exécution (validation métier)")
    try:
        interpreter.interpret("validate_age(-5)")
    except BaobabExecutionException as e:
        print(f"   ❌ {type(e).__name__}: {e}")
        print(f"   Service: {e.service_name}")
        print(f"   Exception originale: {e.original_exception}")
    print()

    # 9. Gestion robuste avec try/except
    print("9. Gestion robuste avec try/except")

    test_cases = [
        ("add(10, 20)", "Cas valide"),
        ("add(10, @)", "Erreur lexicale"),
        ("unknown(42)", "Service inconnu"),
        ("divide(10, 0)", "Division par zéro"),
    ]

    for code, description in test_cases:
        try:
            result = interpreter.interpret(code)
            print(f"   ✅ {description}: {code} = {result}")
        except (
            BaobabLexicalAnalyserException,
            BaobabSyntaxAnalyserException,
            BaobabSemanticAnalyserException,
            BaobabExecutionException,
        ) as e:
            print(f"   ❌ {description}: {type(e).__name__}")

    print()

    print("=" * 60)
    print("Fin de la démonstration")
    print("=" * 60)


if __name__ == "__main__":
    main()
