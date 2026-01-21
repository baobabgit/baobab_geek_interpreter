"""Tests unitaires pour les nœuds AST."""

from typing import Any

from baobab_geek_interpreter.syntax.ast_node import (
    ASTNode,
    ASTVisitor,
    ArgumentNode,
    ArrayNode,
    FloatNode,
    IntNode,
    ServiceCallNode,
    StringNode,
)


class ConcreteVisitor(ASTVisitor):
    """Visiteur concret pour les tests."""

    def visit_service_call(self, node: ServiceCallNode) -> Any:
        """Visite un appel de service."""
        return f"service:{node.name}"

    def visit_argument(self, node: ArgumentNode) -> Any:
        """Visite un argument."""
        return f"arg:{node.value.accept(self)}"

    def visit_int(self, node: IntNode) -> Any:
        """Visite un entier."""
        return f"int:{node.value}"

    def visit_float(self, node: FloatNode) -> Any:
        """Visite un flottant."""
        return f"float:{node.value}"

    def visit_string(self, node: StringNode) -> Any:
        """Visite une chaîne."""
        return f"string:{node.value}"

    def visit_array(self, node: ArrayNode) -> Any:
        """Visite un tableau."""
        elements = [elem.accept(self) for elem in node.elements]
        return f"array:[{','.join(elements)}]"


class TestIntNode:
    """Tests pour IntNode."""

    def test_int_node_init(self) -> None:
        """Vérifie l'initialisation."""
        node = IntNode(42)
        assert node.value == 42

    def test_int_node_with_negative_value(self) -> None:
        """Vérifie avec une valeur négative."""
        node = IntNode(-42)
        assert node.value == -42

    def test_int_node_with_zero(self) -> None:
        """Vérifie avec zéro."""
        node = IntNode(0)
        assert node.value == 0

    def test_int_node_accept(self) -> None:
        """Vérifie la méthode accept."""
        node = IntNode(42)
        visitor = ConcreteVisitor()
        result = node.accept(visitor)
        assert result == "int:42"

    def test_int_node_is_ast_node(self) -> None:
        """Vérifie l'héritage."""
        node = IntNode(42)
        assert isinstance(node, ASTNode)


class TestFloatNode:
    """Tests pour FloatNode."""

    def test_float_node_init(self) -> None:
        """Vérifie l'initialisation."""
        node = FloatNode(3.14)
        assert node.value == 3.14

    def test_float_node_with_negative_value(self) -> None:
        """Vérifie avec une valeur négative."""
        node = FloatNode(-3.14)
        assert node.value == -3.14

    def test_float_node_with_zero(self) -> None:
        """Vérifie avec zéro."""
        node = FloatNode(0.0)
        assert node.value == 0.0

    def test_float_node_accept(self) -> None:
        """Vérifie la méthode accept."""
        node = FloatNode(3.14)
        visitor = ConcreteVisitor()
        result = node.accept(visitor)
        assert result == "float:3.14"

    def test_float_node_is_ast_node(self) -> None:
        """Vérifie l'héritage."""
        node = FloatNode(3.14)
        assert isinstance(node, ASTNode)


class TestStringNode:
    """Tests pour StringNode."""

    def test_string_node_init(self) -> None:
        """Vérifie l'initialisation."""
        node = StringNode("hello")
        assert node.value == "hello"

    def test_string_node_with_empty_string(self) -> None:
        """Vérifie avec une chaîne vide."""
        node = StringNode("")
        assert node.value == ""

    def test_string_node_with_escape_sequences(self) -> None:
        """Vérifie avec des séquences d'échappement."""
        node = StringNode("hello\\nworld")
        assert node.value == "hello\\nworld"

    def test_string_node_accept(self) -> None:
        """Vérifie la méthode accept."""
        node = StringNode("hello")
        visitor = ConcreteVisitor()
        result = node.accept(visitor)
        assert result == "string:hello"

    def test_string_node_is_ast_node(self) -> None:
        """Vérifie l'héritage."""
        node = StringNode("hello")
        assert isinstance(node, ASTNode)


class TestArrayNode:
    """Tests pour ArrayNode."""

    def test_array_node_init_empty(self) -> None:
        """Vérifie l'initialisation avec un tableau vide."""
        node = ArrayNode([])
        assert node.elements == []

    def test_array_node_init_with_ints(self) -> None:
        """Vérifie l'initialisation avec des entiers."""
        elements = [IntNode(1), IntNode(2), IntNode(3)]
        node = ArrayNode(elements)
        assert len(node.elements) == 3
        assert node.elements[0].value == 1
        assert node.elements[1].value == 2
        assert node.elements[2].value == 3

    def test_array_node_init_with_mixed_types(self) -> None:
        """Vérifie l'initialisation avec types mixtes."""
        elements = [IntNode(42), FloatNode(3.14), StringNode("hello")]
        node = ArrayNode(elements)
        assert len(node.elements) == 3

    def test_array_node_accept(self) -> None:
        """Vérifie la méthode accept."""
        elements = [IntNode(1), IntNode(2)]
        node = ArrayNode(elements)
        visitor = ConcreteVisitor()
        result = node.accept(visitor)
        assert result == "array:[int:1,int:2]"

    def test_array_node_accept_empty(self) -> None:
        """Vérifie accept avec un tableau vide."""
        node = ArrayNode([])
        visitor = ConcreteVisitor()
        result = node.accept(visitor)
        assert result == "array:[]"

    def test_array_node_is_ast_node(self) -> None:
        """Vérifie l'héritage."""
        node = ArrayNode([])
        assert isinstance(node, ASTNode)


class TestArgumentNode:
    """Tests pour ArgumentNode."""

    def test_argument_node_init_with_int(self) -> None:
        """Vérifie l'initialisation avec un entier."""
        int_node = IntNode(42)
        arg = ArgumentNode(int_node)
        assert arg.value == int_node
        assert arg.value.value == 42

    def test_argument_node_init_with_float(self) -> None:
        """Vérifie l'initialisation avec un flottant."""
        float_node = FloatNode(3.14)
        arg = ArgumentNode(float_node)
        assert arg.value == float_node

    def test_argument_node_init_with_string(self) -> None:
        """Vérifie l'initialisation avec une chaîne."""
        string_node = StringNode("hello")
        arg = ArgumentNode(string_node)
        assert arg.value == string_node

    def test_argument_node_init_with_array(self) -> None:
        """Vérifie l'initialisation avec un tableau."""
        array_node = ArrayNode([IntNode(1), IntNode(2)])
        arg = ArgumentNode(array_node)
        assert arg.value == array_node

    def test_argument_node_accept(self) -> None:
        """Vérifie la méthode accept."""
        int_node = IntNode(42)
        arg = ArgumentNode(int_node)
        visitor = ConcreteVisitor()
        result = arg.accept(visitor)
        assert result == "arg:int:42"

    def test_argument_node_is_ast_node(self) -> None:
        """Vérifie l'héritage."""
        arg = ArgumentNode(IntNode(42))
        assert isinstance(arg, ASTNode)


class TestServiceCallNode:
    """Tests pour ServiceCallNode."""

    def test_service_call_node_init_no_args(self) -> None:
        """Vérifie l'initialisation sans arguments."""
        node = ServiceCallNode("test_service", [])
        assert node.name == "test_service"
        assert node.arguments == []

    def test_service_call_node_init_with_args(self) -> None:
        """Vérifie l'initialisation avec arguments."""
        args = [ArgumentNode(IntNode(1)), ArgumentNode(IntNode(2))]
        node = ServiceCallNode("add", args)
        assert node.name == "add"
        assert len(node.arguments) == 2

    def test_service_call_node_accept(self) -> None:
        """Vérifie la méthode accept."""
        node = ServiceCallNode("test", [])
        visitor = ConcreteVisitor()
        result = node.accept(visitor)
        assert result == "service:test"

    def test_service_call_node_is_ast_node(self) -> None:
        """Vérifie l'héritage."""
        node = ServiceCallNode("test", [])
        assert isinstance(node, ASTNode)


class TestASTVisitor:
    """Tests pour le pattern Visitor."""

    def test_visitor_can_visit_int(self) -> None:
        """Vérifie la visite d'un entier."""
        visitor = ConcreteVisitor()
        node = IntNode(42)
        result = node.accept(visitor)
        assert result == "int:42"

    def test_visitor_can_visit_float(self) -> None:
        """Vérifie la visite d'un flottant."""
        visitor = ConcreteVisitor()
        node = FloatNode(3.14)
        result = node.accept(visitor)
        assert result == "float:3.14"

    def test_visitor_can_visit_string(self) -> None:
        """Vérifie la visite d'une chaîne."""
        visitor = ConcreteVisitor()
        node = StringNode("hello")
        result = node.accept(visitor)
        assert result == "string:hello"

    def test_visitor_can_visit_array(self) -> None:
        """Vérifie la visite d'un tableau."""
        visitor = ConcreteVisitor()
        elements = [IntNode(1), IntNode(2), IntNode(3)]
        node = ArrayNode(elements)
        result = node.accept(visitor)
        assert result == "array:[int:1,int:2,int:3]"

    def test_visitor_can_visit_argument(self) -> None:
        """Vérifie la visite d'un argument."""
        visitor = ConcreteVisitor()
        arg = ArgumentNode(IntNode(42))
        result = arg.accept(visitor)
        assert result == "arg:int:42"

    def test_visitor_can_visit_service_call(self) -> None:
        """Vérifie la visite d'un appel de service."""
        visitor = ConcreteVisitor()
        node = ServiceCallNode("test", [])
        result = node.accept(visitor)
        assert result == "service:test"

    def test_visitor_can_visit_complex_tree(self) -> None:
        """Vérifie la visite d'un arbre complexe."""
        visitor = ConcreteVisitor()
        args = [
            ArgumentNode(IntNode(42)),
            ArgumentNode(FloatNode(3.14)),
            ArgumentNode(StringNode("hello")),
            ArgumentNode(ArrayNode([IntNode(1), IntNode(2)])),
        ]
        node = ServiceCallNode("complex", args)
        # On vérifie juste que ça ne plante pas
        result = node.accept(visitor)
        assert "service:complex" in result
