"""Exemple d'utilisation avancée avec tableaux et types mixtes."""

from baobab_geek_interpreter import Interpreter, service


def main() -> None:
    """Démonstration de l'utilisation avancée."""
    print("=" * 60)
    print("Baobab Geek Interpreter - Usage Avancé")
    print("=" * 60)
    print()

    interpreter = Interpreter()

    # Services avec tableaux
    @service
    def sum_numbers(numbers: list[int]) -> int:
        """Calcule la somme d'une liste de nombres."""
        return sum(numbers)

    @service
    def average(numbers: list[float]) -> float:
        """Calcule la moyenne d'une liste de nombres."""
        return sum(numbers) / len(numbers) if numbers else 0.0

    @service
    def join_words(words: list[str], separator: str) -> str:
        """Joint des mots avec un séparateur."""
        return separator.join(words)

    @service
    def filter_positive(numbers: list[int]) -> list[int]:
        """Filtre les nombres positifs."""
        return [n for n in numbers if n > 0]

    # Services avec types mixtes
    @service
    def format_price(quantity: int, unit_price: float, product: str) -> str:
        """Formate un prix avec quantité et produit."""
        total = quantity * unit_price
        return f"{quantity} x {product} = ${total:.2f}"

    @service
    def calculate_total(prices: list[float], tax_rate: float) -> float:
        """Calcule le total avec taxes."""
        subtotal = sum(prices)
        return subtotal * (1 + tax_rate)

    # Enregistrer tous les services
    interpreter.register_service("sum_numbers", sum_numbers)
    interpreter.register_service("average", average)
    interpreter.register_service("join_words", join_words)
    interpreter.register_service("filter_positive", filter_positive)
    interpreter.register_service("format_price", format_price)
    interpreter.register_service("calculate_total", calculate_total)

    # Exemples avec tableaux
    print("1. Somme d'un tableau d'entiers")
    result = interpreter.interpret("sum_numbers([1, 2, 3, 4, 5])")
    print(f"   sum_numbers([1, 2, 3, 4, 5]) = {result}")
    print()

    print("2. Moyenne d'un tableau de flottants")
    result = interpreter.interpret("average([1.5, 2.5, 3.5, 4.5])")
    print(f"   average([1.5, 2.5, 3.5, 4.5]) = {result}")
    print()

    print("3. Jointure de mots")
    result = interpreter.interpret('join_words(["Hello", "World", "!"], " ")')
    print(f'   join_words(["Hello", "World", "!"], " ") = {result}')
    print()

    print("4. Filtrage de nombres positifs")
    result = interpreter.interpret("filter_positive([-5, 3, -2, 8, 0, 1])")
    print(f"   filter_positive([-5, 3, -2, 8, 0, 1]) = {result}")
    print()

    # Exemples avec types mixtes
    print("5. Formatage de prix")
    result = interpreter.interpret('format_price(3, 9.99, "apple")')
    print(f'   format_price(3, 9.99, "apple") = {result}')
    print()

    print("6. Calcul de total avec taxes")
    result = interpreter.interpret("calculate_total([10.0, 20.0, 30.0], 0.2)")
    print(f"   calculate_total([10.0, 20.0, 30.0], 0.2) = {result}")
    print()

    # Cas limites
    print("7. Tableau vide")
    result = interpreter.interpret("sum_numbers([])")
    print(f"   sum_numbers([]) = {result}")
    print()

    print("8. Grand tableau")
    result = interpreter.interpret("sum_numbers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])")
    print(f"   sum_numbers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) = {result}")
    print()

    print("=" * 60)
    print("Fin de la démonstration")
    print("=" * 60)


if __name__ == "__main__":
    main()
