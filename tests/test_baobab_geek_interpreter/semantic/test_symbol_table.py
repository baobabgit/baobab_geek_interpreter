"""Tests unitaires pour la classe SymbolTable."""

import pytest
from types import ModuleType

from baobab_geek_interpreter.execution.service_decorator import service
from baobab_geek_interpreter.semantic.symbol_table import SymbolTable


class TestSymbolTableBasics:
    """Tests de base pour SymbolTable."""

    def test_symbol_table_creation(self) -> None:
        """Test la création d'une table des symboles."""
        table = SymbolTable()
        assert table is not None
        assert isinstance(table, SymbolTable)

    def test_empty_table_has_no_services(self) -> None:
        """Test qu'une table vide n'a pas de services."""
        table = SymbolTable()
        assert len(table.list_services()) == 0


class TestSymbolTableRegister:
    """Tests pour l'enregistrement de services."""

    def test_register_single_service(self) -> None:
        """Test l'enregistrement d'un service."""
        table = SymbolTable()

        def my_service() -> str:
            return "result"

        table.register("my_service", my_service)
        assert table.has("my_service")

    def test_register_multiple_services(self) -> None:
        """Test l'enregistrement de plusieurs services."""
        table = SymbolTable()

        def service1() -> int:
            return 1

        def service2() -> int:
            return 2

        table.register("service1", service1)
        table.register("service2", service2)

        assert table.has("service1")
        assert table.has("service2")

    def test_register_overwrites_existing_service(self) -> None:
        """Test que l'enregistrement écrase un service existant."""
        table = SymbolTable()

        def old_service() -> str:
            return "old"

        def new_service() -> str:
            return "new"

        table.register("my_service", old_service)
        table.register("my_service", new_service)

        func = table.get("my_service")
        assert func is not None
        assert func() == "new"

    def test_register_with_lambda(self) -> None:
        """Test l'enregistrement d'une lambda."""
        table = SymbolTable()
        table.register("lambda_service", lambda x: x * 2)

        func = table.get("lambda_service")
        assert func is not None
        assert func(5) == 10


class TestSymbolTableGet:
    """Tests pour la récupération de services."""

    def test_get_existing_service(self) -> None:
        """Test la récupération d'un service existant."""
        table = SymbolTable()

        def add(a: int, b: int) -> int:
            return a + b

        table.register("add", add)
        func = table.get("add")

        assert func is not None
        assert func(3, 5) == 8

    def test_get_non_existing_service_returns_none(self) -> None:
        """Test que get retourne None pour un service inexistant."""
        table = SymbolTable()
        func = table.get("non_existing")
        assert func is None

    def test_get_returns_correct_function(self) -> None:
        """Test que get retourne la bonne fonction."""
        table = SymbolTable()

        def multiply(x: int, y: int) -> int:
            return x * y

        table.register("multiply", multiply)
        func = table.get("multiply")

        assert func is multiply


class TestSymbolTableHas:
    """Tests pour la vérification d'existence de services."""

    def test_has_existing_service(self) -> None:
        """Test has pour un service existant."""
        table = SymbolTable()
        table.register("test", lambda: None)
        assert table.has("test") is True

    def test_has_non_existing_service(self) -> None:
        """Test has pour un service inexistant."""
        table = SymbolTable()
        assert table.has("unknown") is False

    def test_has_after_registration(self) -> None:
        """Test has avant et après enregistrement."""
        table = SymbolTable()
        assert table.has("my_service") is False

        table.register("my_service", lambda: None)
        assert table.has("my_service") is True


class TestSymbolTableListServices:
    """Tests pour le listage des services."""

    def test_list_services_empty_table(self) -> None:
        """Test list_services sur une table vide."""
        table = SymbolTable()
        services = table.list_services()
        assert services == []

    def test_list_services_single_service(self) -> None:
        """Test list_services avec un service."""
        table = SymbolTable()
        table.register("service1", lambda: None)
        services = table.list_services()
        assert services == ["service1"]

    def test_list_services_multiple_services(self) -> None:
        """Test list_services avec plusieurs services."""
        table = SymbolTable()
        table.register("service1", lambda: None)
        table.register("service2", lambda: None)
        table.register("service3", lambda: None)

        services = table.list_services()
        assert len(services) == 3
        assert "service1" in services
        assert "service2" in services
        assert "service3" in services

    def test_list_services_returns_copy(self) -> None:
        """Test que list_services retourne une liste modifiable."""
        table = SymbolTable()
        table.register("service1", lambda: None)

        services1 = table.list_services()
        services1.append("fake")

        services2 = table.list_services()
        assert "fake" not in services2


class TestSymbolTableDiscoverServices:
    """Tests pour la découverte automatique de services."""

    def test_discover_services_in_module(self) -> None:
        """Test la découverte de services dans un module."""
        # Créer un module fictif
        module = ModuleType("test_module")

        @service
        def service1() -> int:
            return 1

        @service
        def service2() -> int:
            return 2

        # Ajouter les services au module
        setattr(module, "service1", service1)
        setattr(module, "service2", service2)

        table = SymbolTable()
        table.discover_services(module)

        assert table.has("service1")
        assert table.has("service2")

    def test_discover_services_ignores_non_services(self) -> None:
        """Test que discover ignore les non-services."""
        module = ModuleType("test_module")

        @service
        def is_service() -> None:
            pass

        def not_service() -> None:
            pass

        setattr(module, "is_service", is_service)
        setattr(module, "not_service", not_service)
        setattr(module, "some_variable", 42)

        table = SymbolTable()
        table.discover_services(module)

        assert table.has("is_service")
        assert not table.has("not_service")
        assert not table.has("some_variable")

    def test_discover_services_empty_module(self) -> None:
        """Test discover sur un module vide."""
        module = ModuleType("empty_module")

        table = SymbolTable()
        table.discover_services(module)

        assert len(table.list_services()) == 0

    def test_discover_services_uses_service_name_attribute(self) -> None:
        """Test que discover utilise l'attribut _service_name."""
        module = ModuleType("test_module")

        @service
        def my_function() -> None:
            pass

        setattr(module, "my_function", my_function)

        table = SymbolTable()
        table.discover_services(module)

        assert table.has("my_function")
        assert table.get("my_function") is my_function


class TestSymbolTableClear:
    """Tests pour la méthode clear."""

    def test_clear_empty_table(self) -> None:
        """Test clear sur une table vide."""
        table = SymbolTable()
        table.clear()
        assert len(table.list_services()) == 0

    def test_clear_removes_all_services(self) -> None:
        """Test que clear supprime tous les services."""
        table = SymbolTable()
        table.register("service1", lambda: None)
        table.register("service2", lambda: None)
        table.register("service3", lambda: None)

        assert len(table.list_services()) == 3

        table.clear()

        assert len(table.list_services()) == 0
        assert not table.has("service1")
        assert not table.has("service2")
        assert not table.has("service3")

    def test_clear_allows_re_registration(self) -> None:
        """Test qu'on peut réenregistrer après clear."""
        table = SymbolTable()
        table.register("service", lambda: "v1")
        table.clear()
        table.register("service", lambda: "v2")

        assert table.has("service")
        func = table.get("service")
        assert func is not None
        assert func() == "v2"


class TestSymbolTableIntegration:
    """Tests d'intégration pour SymbolTable."""

    def test_full_workflow(self) -> None:
        """Test un workflow complet."""
        table = SymbolTable()

        # Enregistrement manuel
        def manual_service(x: int) -> int:
            return x * 2

        table.register("manual", manual_service)

        # Découverte automatique
        module = ModuleType("my_module")

        @service
        def auto_service(x: int) -> int:
            return x + 10

        setattr(module, "auto_service", auto_service)
        table.discover_services(module)

        # Vérifications
        assert table.has("manual")
        assert table.has("auto_service")
        assert len(table.list_services()) == 2

        # Exécution
        manual_func = table.get("manual")
        auto_func = table.get("auto_service")
        assert manual_func is not None
        assert auto_func is not None
        assert manual_func(5) == 10
        assert auto_func(5) == 15

    def test_multiple_modules_discovery(self) -> None:
        """Test la découverte dans plusieurs modules."""
        table = SymbolTable()

        # Module 1
        module1 = ModuleType("module1")

        @service
        def service1() -> str:
            return "m1"

        setattr(module1, "service1", service1)

        # Module 2
        module2 = ModuleType("module2")

        @service
        def service2() -> str:
            return "m2"

        setattr(module2, "service2", service2)

        # Découverte
        table.discover_services(module1)
        table.discover_services(module2)

        assert table.has("service1")
        assert table.has("service2")
        assert len(table.list_services()) == 2
