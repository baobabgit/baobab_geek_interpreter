"""Exemple de création de services personnalisés."""

from baobab_geek_interpreter import Interpreter, service


# Module de services personnalisés
class MathServices:
    """Services mathématiques."""

    @staticmethod
    @service
    def factorial(n: int) -> int:
        """Calcule la factorielle de n."""
        if n < 0:
            raise ValueError("n doit être positif")
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    @service
    def fibonacci(n: int) -> int:
        """Calcule le n-ième nombre de Fibonacci."""
        if n < 0:
            raise ValueError("n doit être positif")
        if n == 0:
            return 0
        if n == 1:
            return 1
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


class StringServices:
    """Services de manipulation de chaînes."""

    @staticmethod
    @service
    def reverse(text: str) -> str:
        """Inverse une chaîne de caractères."""
        return text[::-1]

    @staticmethod
    @service
    def to_upper(text: str) -> str:
        """Convertit en majuscules."""
        return text.upper()

    @staticmethod
    @service
    def count_words(text: str) -> int:
        """Compte le nombre de mots."""
        return len(text.split())


class ListServices:
    """Services de manipulation de listes."""

    @staticmethod
    @service
    def max_value(numbers: list[int]) -> int:
        """Trouve le maximum d'une liste."""
        if not numbers:
            raise ValueError("La liste ne peut pas être vide")
        return max(numbers)

    @staticmethod
    @service
    def min_value(numbers: list[int]) -> int:
        """Trouve le minimum d'une liste."""
        if not numbers:
            raise ValueError("La liste ne peut pas être vide")
        return min(numbers)

    @staticmethod
    @service
    def sort_numbers(numbers: list[int]) -> list[int]:
        """Trie une liste de nombres."""
        return sorted(numbers)


def main() -> None:
    """Démonstration de services personnalisés."""
    print("=" * 60)
    print("Baobab Geek Interpreter - Services Personnalisés")
    print("=" * 60)
    print()

    interpreter = Interpreter()

    # Enregistrer les services depuis les classes
    print("Enregistrement des services...")

    # Méthode 1 : Enregistrement manuel
    interpreter.register_service("factorial", MathServices.factorial)
    interpreter.register_service("fibonacci", MathServices.fibonacci)
    interpreter.register_service("reverse", StringServices.reverse)
    interpreter.register_service("to_upper", StringServices.to_upper)
    interpreter.register_service("count_words", StringServices.count_words)
    interpreter.register_service("max_value", ListServices.max_value)
    interpreter.register_service("min_value", ListServices.min_value)
    interpreter.register_service("sort_numbers", ListServices.sort_numbers)

    print(f"✅ {len(interpreter.list_services())} services enregistrés")
    print()

    # Services mathématiques
    print("1. Services mathématiques")
    print(f"   factorial(5) = {interpreter.interpret('factorial(5)')}")
    print(f"   fibonacci(10) = {interpreter.interpret('fibonacci(10)')}")
    print()

    # Services de chaînes
    print("2. Services de chaînes")
    result = interpreter.interpret('reverse("Hello")')
    print(f'   reverse("Hello") = {result}')
    result = interpreter.interpret('to_upper("hello")')
    print(f'   to_upper("hello") = {result}')
    result = interpreter.interpret('count_words("Hello World !")')
    print(f'   count_words("Hello World !") = {result}')
    print()

    # Services de listes
    print("3. Services de listes")
    print(
        f"   max_value([5, 2, 9, 1, 7]) = " f"{interpreter.interpret('max_value([5, 2, 9, 1, 7])')}"
    )
    print(
        f"   min_value([5, 2, 9, 1, 7]) = " f"{interpreter.interpret('min_value([5, 2, 9, 1, 7])')}"
    )
    print(
        f"   sort_numbers([5, 2, 9, 1, 7]) = "
        f"{interpreter.interpret('sort_numbers([5, 2, 9, 1, 7])')}"
    )
    print()

    # Cas d'usage réel : traitement de données
    print("4. Cas d'usage réel : analyse de données")

    # Simuler des données de ventes
    sales_data = [120, 85, 200, 150, 95, 180, 110]

    print(f"   Données de ventes : {sales_data}")
    print(f"   Maximum : " f"{interpreter.interpret(f'max_value({sales_data})')}")
    print(f"   Minimum : " f"{interpreter.interpret(f'min_value({sales_data})')}")
    print()

    # Liste des services disponibles
    print("5. Services disponibles:")
    for i, service_name in enumerate(sorted(interpreter.list_services()), 1):
        print(f"   {i}. {service_name}")
    print()

    print("=" * 60)
    print("Fin de la démonstration")
    print("=" * 60)


if __name__ == "__main__":
    main()
