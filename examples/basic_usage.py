"""Exemple d'utilisation basique de Baobab Geek Interpreter."""

from baobab_geek_interpreter import Interpreter, service


def main() -> None:
    """Démonstration de l'utilisation basique."""
    print("=" * 60)
    print("Baobab Geek Interpreter - Usage Basique")
    print("=" * 60)
    print()

    # Créer l'interpréteur
    interpreter = Interpreter()

    # Définir des services simples
    @service
    def add(a: int, b: int) -> int:
        """Additionne deux nombres."""
        return a + b

    @service
    def subtract(a: int, b: int) -> int:
        """Soustrait deux nombres."""
        return a - b

    @service
    def multiply(a: float, b: float) -> float:
        """Multiplie deux nombres."""
        return a * b

    @service
    def greet(name: str) -> str:
        """Salue une personne."""
        return f"Hello, {name}!"

    # Enregistrer les services
    interpreter.register_service("add", add)
    interpreter.register_service("subtract", subtract)
    interpreter.register_service("multiply", multiply)
    interpreter.register_service("greet", greet)

    # Exemples d'utilisation
    print("1. Addition de deux entiers")
    result = interpreter.interpret("add(10, 20)")
    print(f"   add(10, 20) = {result}")
    print()

    print("2. Soustraction avec nombres négatifs")
    result = interpreter.interpret("subtract(-5, -3)")
    print(f"   subtract(-5, -3) = {result}")
    print()

    print("3. Multiplication de flottants")
    result = interpreter.interpret("multiply(2.5, 4.0)")
    print(f"   multiply(2.5, 4.0) = {result}")
    print()

    print("4. Salutation avec chaîne")
    result = interpreter.interpret('greet("Alice")')
    print(f'   greet("Alice") = {result}')
    print()

    # Lister les services disponibles
    print("5. Services disponibles:")
    for service_name in interpreter.list_services():
        print(f"   - {service_name}")
    print()

    print("=" * 60)
    print("Fin de la démonstration")
    print("=" * 60)


if __name__ == "__main__":
    main()
