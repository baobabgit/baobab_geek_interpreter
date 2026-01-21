"""Tests unitaires pour la classe TypeChecker."""

import pytest

from baobab_geek_interpreter.semantic.type_checker import TypeChecker


class TestTypeCheckerBasics:
    """Tests de base pour TypeChecker."""

    def test_check_types_with_matching_int_args(self) -> None:
        """Test avec arguments entiers correspondants."""

        def func(a: int, b: int) -> int:
            return a + b

        assert TypeChecker.check_types(func, [1, 2]) is True

    def test_check_types_with_mismatched_types(self) -> None:
        """Test avec types non correspondants."""

        def func(a: int, b: str) -> None:
            pass

        assert TypeChecker.check_types(func, [1, 2]) is False
        assert TypeChecker.check_types(func, ["hello", "world"]) is False

    def test_check_types_with_wrong_number_of_args(self) -> None:
        """Test avec mauvais nombre d'arguments."""

        def func(a: int, b: int) -> int:
            return a + b

        assert TypeChecker.check_types(func, [1]) is False
        assert TypeChecker.check_types(func, [1, 2, 3]) is False

    def test_check_types_without_annotations(self) -> None:
        """Test avec fonction sans annotations de type."""

        def func(a, b):  # type: ignore
            return a + b

        # Sans annotations, on accepte tout
        assert TypeChecker.check_types(func, [1, 2]) is True
        assert TypeChecker.check_types(func, ["hello", "world"]) is True


class TestTypeCheckerSimpleTypes:
    """Tests pour les types simples."""

    def test_check_int_type(self) -> None:
        """Test du type int."""

        def func(x: int) -> None:
            pass

        assert TypeChecker.check_types(func, [42]) is True
        assert TypeChecker.check_types(func, [-10]) is True
        assert TypeChecker.check_types(func, [3.14]) is False
        assert TypeChecker.check_types(func, ["42"]) is False

    def test_check_float_type(self) -> None:
        """Test du type float."""

        def func(x: float) -> None:
            pass

        assert TypeChecker.check_types(func, [3.14]) is True
        assert TypeChecker.check_types(func, [-2.5]) is True
        assert TypeChecker.check_types(func, [42]) is False  # Pas de conversion auto
        assert TypeChecker.check_types(func, ["3.14"]) is False

    def test_check_str_type(self) -> None:
        """Test du type str."""

        def func(x: str) -> None:
            pass

        assert TypeChecker.check_types(func, ["hello"]) is True
        assert TypeChecker.check_types(func, [""]) is True
        assert TypeChecker.check_types(func, [42]) is False
        assert TypeChecker.check_types(func, [3.14]) is False

    def test_check_mixed_types(self) -> None:
        """Test avec types mixtes."""

        def func(a: int, b: float, c: str) -> None:
            pass

        assert TypeChecker.check_types(func, [1, 2.5, "text"]) is True
        assert TypeChecker.check_types(func, [1, 2, "text"]) is False


class TestTypeCheckerListTypes:
    """Tests pour les types list[T]."""

    def test_check_list_int_type(self) -> None:
        """Test du type list[int]."""

        def func(x: list[int]) -> None:
            pass

        assert TypeChecker.check_types(func, [[1, 2, 3]]) is True
        assert TypeChecker.check_types(func, [[]]) is True  # Liste vide
        assert TypeChecker.check_types(func, [[1, 2.5, 3]]) is False
        assert TypeChecker.check_types(func, [[1, "2", 3]]) is False
        assert TypeChecker.check_types(func, [42]) is False  # Pas une liste

    def test_check_list_float_type(self) -> None:
        """Test du type list[float]."""

        def func(x: list[float]) -> None:
            pass

        assert TypeChecker.check_types(func, [[1.5, 2.5, 3.5]]) is True
        assert TypeChecker.check_types(func, [[1, 2, 3]]) is False  # Pas de conversion

    def test_check_list_str_type(self) -> None:
        """Test du type list[str]."""

        def func(x: list[str]) -> None:
            pass

        assert TypeChecker.check_types(func, [["a", "b", "c"]]) is True
        assert TypeChecker.check_types(func, [["a", 1, "c"]]) is False

    def test_check_multiple_lists(self) -> None:
        """Test avec plusieurs listes."""

        def func(a: list[int], b: list[str]) -> None:
            pass

        assert TypeChecker.check_types(func, [[1, 2], ["a", "b"]]) is True
        assert TypeChecker.check_types(func, [[1, 2], [1, 2]]) is False


class TestArrayHomogeneity:
    """Tests pour l'homogénéité des tableaux."""

    def test_is_array_homogeneous_with_ints(self) -> None:
        """Test avec tableau d'entiers."""
        assert TypeChecker.is_array_homogeneous([1, 2, 3]) is True
        assert TypeChecker.is_array_homogeneous([1]) is True

    def test_is_array_homogeneous_with_floats(self) -> None:
        """Test avec tableau de flottants."""
        assert TypeChecker.is_array_homogeneous([1.5, 2.5, 3.5]) is True

    def test_is_array_homogeneous_with_strings(self) -> None:
        """Test avec tableau de chaînes."""
        assert TypeChecker.is_array_homogeneous(["a", "b", "c"]) is True

    def test_is_array_homogeneous_with_mixed_types(self) -> None:
        """Test avec types mixtes."""
        assert TypeChecker.is_array_homogeneous([1, "2", 3]) is False
        assert TypeChecker.is_array_homogeneous([1, 2.5, 3]) is False
        assert TypeChecker.is_array_homogeneous([1.0, "hello", True]) is False

    def test_is_array_homogeneous_empty_array(self) -> None:
        """Test avec tableau vide."""
        assert TypeChecker.is_array_homogeneous([]) is True


class TestNestedArrays:
    """Tests pour la détection de tableaux imbriqués."""

    def test_has_nested_arrays_simple_array(self) -> None:
        """Test avec tableau simple."""
        assert TypeChecker.has_nested_arrays([1, 2, 3]) is False
        assert TypeChecker.has_nested_arrays(["a", "b"]) is False

    def test_has_nested_arrays_with_nesting(self) -> None:
        """Test avec tableaux imbriqués."""
        assert TypeChecker.has_nested_arrays([[1, 2], [3, 4]]) is True
        assert TypeChecker.has_nested_arrays([[1]]) is True
        assert TypeChecker.has_nested_arrays([[]]) is True

    def test_has_nested_arrays_partial_nesting(self) -> None:
        """Test avec imbrication partielle."""
        assert TypeChecker.has_nested_arrays([1, [2, 3]]) is True

    def test_has_nested_arrays_empty_array(self) -> None:
        """Test avec tableau vide."""
        assert TypeChecker.has_nested_arrays([]) is False


class TestGetArrayElementType:
    """Tests pour l'extraction du type d'éléments."""

    def test_get_array_element_type_int(self) -> None:
        """Test avec tableau d'entiers."""
        assert TypeChecker.get_array_element_type([1, 2, 3]) == int

    def test_get_array_element_type_float(self) -> None:
        """Test avec tableau de flottants."""
        assert TypeChecker.get_array_element_type([1.5, 2.5]) == float

    def test_get_array_element_type_str(self) -> None:
        """Test avec tableau de chaînes."""
        assert TypeChecker.get_array_element_type(["a", "b"]) == str

    def test_get_array_element_type_empty_array_raises(self) -> None:
        """Test qu'un tableau vide lève une exception."""
        with pytest.raises(ValueError, match="empty array"):
            TypeChecker.get_array_element_type([])

    def test_get_array_element_type_heterogeneous_raises(self) -> None:
        """Test qu'un tableau hétérogène lève une exception."""
        with pytest.raises(ValueError, match="not homogeneous"):
            TypeChecker.get_array_element_type([1, "2", 3])


class TestCheckSingleType:
    """Tests pour la vérification d'un type individuel."""

    def test_check_single_type_int(self) -> None:
        """Test avec entier."""
        assert TypeChecker._check_single_type(42, int) is True
        assert TypeChecker._check_single_type("42", int) is False

    def test_check_single_type_float(self) -> None:
        """Test avec flottant."""
        assert TypeChecker._check_single_type(3.14, float) is True
        assert TypeChecker._check_single_type(3, float) is False

    def test_check_single_type_str(self) -> None:
        """Test avec chaîne."""
        assert TypeChecker._check_single_type("hello", str) is True
        assert TypeChecker._check_single_type(42, str) is False

    def test_check_single_type_list(self) -> None:
        """Test avec liste."""
        assert TypeChecker._check_single_type([1, 2], list[int]) is True
        assert TypeChecker._check_single_type([1, "2"], list[int]) is False
        assert TypeChecker._check_single_type(42, list[int]) is False
