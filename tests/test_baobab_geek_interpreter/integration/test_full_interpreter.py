"""Tests d'intégration bout-en-bout pour l'interpréteur complet."""

import pytest

from baobab_geek_interpreter import (
    BaobabExecutionException,
    BaobabLexicalAnalyserException,
    BaobabSemanticAnalyserException,
    BaobabSyntaxAnalyserException,
    Interpreter,
    service,
)


class TestFullInterpreterBasicUsage:
    """Tests d'intégration pour l'usage basique."""

    def test_complete_workflow_addition(self) -> None:
        """Test du workflow complet pour une addition."""
        # Créer l'interpréteur
        interpreter = Interpreter()

        # Définir un service
        @service
        def add(a: int, b: int) -> int:
            """Additionne deux nombres."""
            return a + b

        # Enregistrer le service
        interpreter.register_service("add", add)

        # Interpréter et exécuter
        result = interpreter.interpret("add(10, 20)")

        # Vérifier le résultat
        assert result == 30

    def test_complete_workflow_string_operations(self) -> None:
        """Test du workflow complet pour des opérations sur chaînes."""
        interpreter = Interpreter()

        @service
        def concat(a: str, b: str) -> str:
            return a + b

        @service
        def repeat(text: str, count: int) -> str:
            return text * count

        interpreter.register_service("concat", concat)
        interpreter.register_service("repeat", repeat)

        result1 = interpreter.interpret('concat("Hello", " World")')
        assert result1 == "Hello World"

        result2 = interpreter.interpret('repeat("Hi", 3)')
        assert result2 == "HiHiHi"

    def test_complete_workflow_array_operations(self) -> None:
        """Test du workflow complet pour des opérations sur tableaux."""
        interpreter = Interpreter()

        @service
        def sum_numbers(numbers: list[int]) -> int:
            return sum(numbers)

        @service
        def average(numbers: list[float]) -> float:
            return sum(numbers) / len(numbers) if numbers else 0.0

        interpreter.register_service("sum_numbers", sum_numbers)
        interpreter.register_service("average", average)

        result1 = interpreter.interpret("sum_numbers([1, 2, 3, 4, 5])")
        assert result1 == 15

        result2 = interpreter.interpret("average([1.0, 2.0, 3.0, 4.0])")
        assert result2 == 2.5


class TestFullInterpreterModuleRegistration:
    """Tests d'intégration pour l'enregistrement de modules."""

    def test_register_services_from_module(self) -> None:
        """Test l'enregistrement automatique depuis un module."""

        # Créer un module simulé avec plusieurs services
        # Note: Les fonctions doivent être au niveau module, pas dans une classe
        @service
        def add(a: int, b: int) -> int:
            return a + b

        @service
        def multiply(a: int, b: int) -> int:
            return a * b

        @service
        def concat(a: str, b: str) -> str:
            return a + b

        def not_a_service(x: int) -> int:
            return x

        # Créer un objet module simulé
        class FakeModule:
            pass

        fake_module = FakeModule()
        fake_module.add = add  # type: ignore
        fake_module.multiply = multiply  # type: ignore
        fake_module.concat = concat  # type: ignore
        fake_module.not_a_service = not_a_service  # type: ignore

        interpreter = Interpreter()
        interpreter.register_services(fake_module)

        # Vérifier que les services sont enregistrés
        assert interpreter.has_service("add")
        assert interpreter.has_service("multiply")
        assert interpreter.has_service("concat")
        assert not interpreter.has_service("not_a_service")

        # Tester l'exécution
        assert interpreter.interpret("add(5, 3)") == 8
        assert interpreter.interpret("multiply(4, 7)") == 28
        assert interpreter.interpret('concat("A", "B")') == "AB"


class TestFullInterpreterErrorHandling:
    """Tests d'intégration pour la gestion des erreurs."""

    def test_error_handling_lexical(self) -> None:
        """Test la gestion des erreurs lexicales."""
        interpreter = Interpreter()

        @service
        def test_func(x: int) -> int:
            return x

        interpreter.register_service("test_func", test_func)

        with pytest.raises(BaobabLexicalAnalyserException):
            interpreter.interpret("test_func(@)")

    def test_error_handling_syntax(self) -> None:
        """Test la gestion des erreurs syntaxiques."""
        interpreter = Interpreter()

        @service
        def test_func(x: int) -> int:
            return x

        interpreter.register_service("test_func", test_func)

        with pytest.raises(BaobabSyntaxAnalyserException):
            interpreter.interpret("test_func(")

    def test_error_handling_semantic_unknown_service(self) -> None:
        """Test la gestion d'un service inconnu."""
        interpreter = Interpreter()

        with pytest.raises(BaobabSemanticAnalyserException, match="Service inconnu"):
            interpreter.interpret("unknown(10)")

    def test_error_handling_semantic_type_mismatch(self) -> None:
        """Test la gestion d'une incompatibilité de types."""
        interpreter = Interpreter()

        @service
        def add(a: int, b: int) -> int:
            return a + b

        interpreter.register_service("add", add)

        with pytest.raises(
            BaobabSemanticAnalyserException, match="Types d'arguments incompatibles"
        ):
            interpreter.interpret('add(10, "20")')

    def test_error_handling_execution(self) -> None:
        """Test la gestion des erreurs d'exécution."""
        interpreter = Interpreter()

        @service
        def divide(a: int, b: int) -> float:
            return a / b

        interpreter.register_service("divide", divide)

        with pytest.raises(BaobabExecutionException) as exc_info:
            interpreter.interpret("divide(10, 0)")

        assert "divide" in str(exc_info.value)
        assert exc_info.value.service_name == "divide"


class TestFullInterpreterRealWorldScenarios:
    """Tests d'intégration pour des scénarios réels."""

    def test_real_world_shopping_cart(self) -> None:
        """Test un scénario réel de panier d'achat."""
        interpreter = Interpreter()

        @service
        def calculate_total(prices: list[float], tax_rate: float) -> float:
            subtotal = sum(prices)
            return subtotal * (1 + tax_rate)

        @service
        def apply_discount(total: float, discount_percent: float) -> float:
            return total * (1 - discount_percent / 100)

        interpreter.register_service("calculate_total", calculate_total)
        interpreter.register_service("apply_discount", apply_discount)

        # Calculer le total avec taxes
        total = interpreter.interpret("calculate_total([10.0, 20.0, 30.0], 0.2)")
        assert total == 72.0

        # Appliquer une réduction
        final = interpreter.interpret("apply_discount(72.0, 10.0)")
        assert final == 64.8

    def test_real_world_data_processing(self) -> None:
        """Test un scénario réel de traitement de données."""
        interpreter = Interpreter()

        @service
        def filter_positive(numbers: list[int]) -> list[int]:
            return [n for n in numbers if n > 0]

        @service
        def double_values(numbers: list[int]) -> list[int]:
            return [n * 2 for n in numbers]

        @service
        def max_value(numbers: list[int]) -> int:
            return max(numbers) if numbers else 0

        interpreter.register_service("filter_positive", filter_positive)
        interpreter.register_service("double_values", double_values)
        interpreter.register_service("max_value", max_value)

        # Filtrer les positifs
        filtered = interpreter.interpret("filter_positive([-5, 3, -2, 8, 0, 1])")
        assert filtered == [3, 8, 1]

        # Doubler les valeurs
        doubled = interpreter.interpret("double_values([1, 2, 3])")
        assert doubled == [2, 4, 6]

        # Trouver le maximum
        maximum = interpreter.interpret("max_value([5, 2, 9, 1, 7])")
        assert maximum == 9

    def test_real_world_text_processing(self) -> None:
        """Test un scénario réel de traitement de texte."""
        interpreter = Interpreter()

        @service
        def join_words(words: list[str], separator: str) -> str:
            return separator.join(words)

        @service
        def count_words(words: list[str]) -> int:
            return len(words)

        @service
        def filter_long_words(words: list[str], min_length: int) -> list[str]:
            return [w for w in words if len(w) >= min_length]

        interpreter.register_service("join_words", join_words)
        interpreter.register_service("count_words", count_words)
        interpreter.register_service("filter_long_words", filter_long_words)

        # Joindre des mots
        joined = interpreter.interpret('join_words(["Hello", "World"], " ")')
        assert joined == "Hello World"

        # Compter les mots
        count = interpreter.interpret('count_words(["one", "two", "three"])')
        assert count == 3

        # Filtrer les mots longs
        filtered = interpreter.interpret('filter_long_words(["hi", "hello", "hey", "world"], 5)')
        assert filtered == ["hello", "world"]


class TestFullInterpreterEdgeCases:
    """Tests d'intégration pour les cas limites."""

    def test_edge_case_empty_arrays(self) -> None:
        """Test avec des tableaux vides."""
        interpreter = Interpreter()

        @service
        def process_empty(items: list[int]) -> int:
            return len(items)

        interpreter.register_service("process_empty", process_empty)
        result = interpreter.interpret("process_empty([])")
        assert result == 0

    def test_edge_case_negative_numbers(self) -> None:
        """Test avec des nombres négatifs."""
        interpreter = Interpreter()

        @service
        def subtract(a: int, b: int) -> int:
            return a - b

        interpreter.register_service("subtract", subtract)
        result = interpreter.interpret("subtract(-10, -5)")
        assert result == -5

    def test_edge_case_large_arrays(self) -> None:
        """Test avec de grands tableaux."""
        interpreter = Interpreter()

        @service
        def sum_large(numbers: list[int]) -> int:
            return sum(numbers)

        interpreter.register_service("sum_large", sum_large)
        result = interpreter.interpret("sum_large([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])")
        assert result == 55

    def test_edge_case_service_returns_none(self) -> None:
        """Test avec un service retournant None."""
        interpreter = Interpreter()

        executed = []

        @service
        def log_message(message: str) -> None:
            executed.append(message)

        interpreter.register_service("log_message", log_message)
        result = interpreter.interpret('log_message("Test")')
        assert result is None
        assert executed == ["Test"]

    def test_edge_case_service_returns_list(self) -> None:
        """Test avec un service retournant une liste."""
        interpreter = Interpreter()

        @service
        def create_range(start: int, end: int) -> list[int]:
            return list(range(start, end))

        interpreter.register_service("create_range", create_range)
        result = interpreter.interpret("create_range(1, 6)")
        assert result == [1, 2, 3, 4, 5]


class TestFullInterpreterServiceManagement:
    """Tests d'intégration pour la gestion des services."""

    def test_service_management_list_clear(self) -> None:
        """Test la gestion des services (liste, suppression)."""
        interpreter = Interpreter()

        @service
        def service1(x: int) -> int:
            return x

        @service
        def service2(x: int) -> int:
            return x * 2

        # Enregistrer des services
        interpreter.register_service("service1", service1)
        interpreter.register_service("service2", service2)

        # Vérifier la liste
        services = interpreter.list_services()
        assert len(services) == 2
        assert "service1" in services
        assert "service2" in services

        # Supprimer tous les services
        interpreter.clear_services()
        assert len(interpreter.list_services()) == 0

    def test_service_management_overwrite(self) -> None:
        """Test l'écrasement d'un service."""
        interpreter = Interpreter()

        @service
        def my_service(x: int) -> int:
            return x

        @service
        def my_service_v2(x: int) -> int:
            return x * 2

        # Enregistrer la première version
        interpreter.register_service("my_service", my_service)
        result1 = interpreter.interpret("my_service(5)")
        assert result1 == 5

        # Écraser avec la deuxième version
        interpreter.register_service("my_service", my_service_v2)
        result2 = interpreter.interpret("my_service(5)")
        assert result2 == 10


class TestFullInterpreterComplexWorkflows:
    """Tests d'intégration pour des workflows complexes."""

    def test_complex_workflow_multi_step(self) -> None:
        """Test un workflow complexe en plusieurs étapes."""
        interpreter = Interpreter()

        @service
        def step1_filter(numbers: list[int], threshold: int) -> list[int]:
            return [n for n in numbers if n > threshold]

        @service
        def step2_transform(numbers: list[int], factor: int) -> list[int]:
            return [n * factor for n in numbers]

        @service
        def step3_aggregate(numbers: list[int]) -> int:
            return sum(numbers)

        interpreter.register_service("step1_filter", step1_filter)
        interpreter.register_service("step2_transform", step2_transform)
        interpreter.register_service("step3_aggregate", step3_aggregate)

        # Étape 1 : Filtrer
        filtered = interpreter.interpret("step1_filter([1, 5, 3, 8, 2, 9], 4)")
        assert filtered == [5, 8, 9]

        # Étape 2 : Transformer (simulé avec les résultats de l'étape 1)
        transformed = interpreter.interpret("step2_transform([5, 8, 9], 2)")
        assert transformed == [10, 16, 18]

        # Étape 3 : Agréger (simulé avec les résultats de l'étape 2)
        result = interpreter.interpret("step3_aggregate([10, 16, 18])")
        assert result == 44
