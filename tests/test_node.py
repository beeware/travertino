from unittest.mock import Mock

import pytest

from tests.utils import mock_attr, prep_style_class
from travertino.declaration import BaseStyle, Choices, validated_property
from travertino.layout import BaseBox, Viewport
from travertino.node import Node
from travertino.size import BaseIntrinsicSize


@prep_style_class
@mock_attr("reapply")
class Style(BaseStyle):
    int_prop: int = validated_property(Choices(integer=True))

    class IntrinsicSize(BaseIntrinsicSize):
        pass

    class Box(BaseBox):
        pass

    def layout(self, root, viewport):
        # A simple layout scheme that allocates twice the viewport size.
        root.layout.content_width = viewport.width * 2
        root.layout.content_height = viewport.height * 2


@prep_style_class
class BrokenStyle(BaseStyle):
    def reapply(self):
        raise AttributeError("Missing attribute, node not ready for style application")

    class IntrinsicSize(BaseIntrinsicSize):
        pass

    class Box(BaseBox):
        pass

    def layout(self, root, viewport):
        # A simple layout scheme that allocates twice the viewport size.
        root.layout.content_width = viewport.width * 2
        root.layout.content_height = viewport.height * 2


def test_create_leaf():
    """A leaf can be created"""
    style = Style()
    leaf = Node(style=style)

    assert leaf._children is None
    assert leaf.children == []
    assert not leaf.can_have_children

    # An unattached leaf is a root
    assert leaf.parent is None
    assert leaf.root == leaf

    # A leaf can't have children
    child = Node(style=style)

    with pytest.raises(ValueError):
        leaf.add(child)


def test_create_node():
    """A node can be created with children"""
    style = Style()

    child1 = Node(style=style)
    child2 = Node(style=style)
    child3 = Node(style=style)

    node = Node(style=style, children=[child1, child2, child3])

    assert node.children == [child1, child2, child3]
    assert node.can_have_children

    # The node is the root as well.
    assert node.parent is None
    assert node.root == node

    # The children all point at the node.
    assert child1.parent == node
    assert child1.root == node

    assert child2.parent == node
    assert child2.root == node

    assert child3.parent == node
    assert child3.root == node

    # Create another node
    new_node = Node(style=style, children=[])

    assert new_node.children == []
    assert new_node.can_have_children

    # Add the old node as a child of the new one.
    new_node.add(node)

    # The new node is the root
    assert new_node.parent is None
    assert new_node.root == new_node

    # The node is the root as well.
    assert node.parent == new_node
    assert node.root == new_node

    # The children all point at the node.
    assert child1.parent == node
    assert child1.root == new_node

    assert child2.parent == node
    assert child2.root == new_node

    assert child3.parent == node
    assert child3.root == new_node


def test_refresh():
    """The layout can be refreshed, and the applicator invoked"""

    # Define an applicator that tracks the node being rendered and its size
    class Applicator:
        def __init__(self, node):
            self.tasks = []
            self.node = node

        def set_bounds(self):
            self.tasks.append(
                (
                    self.node,
                    self.node.layout.content_width,
                    self.node.layout.content_height,
                )
            )

    class TestNode(Node):
        def __init__(self, style, children=None):
            super().__init__(
                style=style, applicator=Applicator(self), children=children
            )

    # Define a simple 2 level tree of nodes.
    style = Style()
    child1 = TestNode(style=style)
    child2 = TestNode(style=style)
    child3 = TestNode(style=style)

    node = TestNode(style=style, children=[child1, child2, child3])

    # Refresh the root node
    node.refresh(Viewport(width=10, height=20))

    # Check the output is as expected
    assert node.applicator.tasks == [(node, 20, 40)]
    assert child1.applicator.tasks == []
    assert child2.applicator.tasks == []
    assert child3.applicator.tasks == []

    # Reset the applicator
    node.applicator.tasks = []

    # Refresh a child node
    child1.refresh(Viewport(width=15, height=25))

    # The root node was rendered, not the child.
    assert node.applicator.tasks == [(node, 30, 50)]
    assert child1.applicator.tasks == []
    assert child2.applicator.tasks == []
    assert child3.applicator.tasks == []


def test_add():
    """Nodes can be added as children to another node"""

    style = Style()
    node = Node(style=style, children=[])

    child = Node(style=style)
    node.add(child)

    assert child in node.children
    assert child.parent == node
    assert child.root == node.root


def test_insert():
    """Node can be inserted at a specific position as a child"""

    style = Style()
    child1 = Node(style=style)
    child2 = Node(style=style)
    child3 = Node(style=style)
    node = Node(style=style, children=[child1, child2, child3])

    child4 = Node(style=style)

    index = 2
    node.insert(index, child4)

    assert child4 in node.children
    assert child4.parent == node
    assert child4.root == node.root

    assert node.children.index(child4) == index


def test_remove():
    """Children can be removed from node"""

    style = Style()
    child1 = Node(style=style)
    child2 = Node(style=style)
    child3 = Node(style=style)
    node = Node(style=style, children=[child1, child2, child3])

    node.remove(child1)

    assert child1 not in node.children
    assert child1.parent is None
    assert child1.root == child1


def test_clear():
    """Node can be inserted at a specific position as a child"""
    style = Style()
    children = [Node(style=style), Node(style=style), Node(style=style)]
    node = Node(style=style, children=children)

    for child in children:
        assert child in node.children
        assert child.parent == node
        assert child.root == node
    assert node.children == children

    node.clear()

    for child in children:
        assert child not in node.children
        assert child.parent is None
        assert child.root == child

    assert node.children == []


def test_create_with_no_applicator():
    style = Style(int_prop=5)
    node = Node(style=style)

    # Style copies on assignment.
    assert isinstance(node.style, Style)
    assert node.style == style
    assert node.style is not style

    # Since no applicator has been assigned, style wasn't applied.
    node.style.reapply.assert_not_called()


def test_create_with_applicator():
    style = Style(int_prop=5)
    applicator = Mock()
    node = Node(style=style, applicator=applicator)

    # Style copies on assignment.
    assert isinstance(node.style, Style)
    assert node.style == style
    assert node.style is not style

    # Applicator assignment does *not* copy.
    assert node.applicator is applicator
    # Applicator gets a reference back to its node and to the style.
    assert applicator.node is node
    assert node.style._applicator is applicator

    # Assigning a non-None applicator should always apply style.
    node.style.reapply.assert_called_once()


@pytest.mark.parametrize(
    "node",
    [
        Node(style=Style()),
        Node(style=Style(), applicator=Mock()),
    ],
)
def test_assign_applicator(node):
    node.style.reapply.reset_mock()

    applicator = Mock()
    node.applicator = applicator

    # Applicator assignment does *not* copy.
    assert node.applicator is applicator
    # Applicator gets a reference back to its node and to the style.
    assert applicator.node is node
    assert node.style._applicator is applicator

    # Assigning a non-None applicator should always apply style.
    node.style.reapply.assert_called_once()


@pytest.mark.parametrize(
    "node",
    [
        Node(style=Style()),
        Node(style=Style(), applicator=Mock()),
    ],
)
def test_assign_applicator_none(node):
    node.style.reapply.reset_mock()

    node.applicator = None
    assert node.applicator is None

    # Should be updated on style as well
    assert node.style._applicator is None
    # Assigning None to applicator does not trigger reapply.
    node.style.reapply.assert_not_called()


def test_assign_style_with_applicator():
    style_1 = Style(int_prop=5)
    node = Node(style=style_1, applicator=Mock())

    node.style.reapply.reset_mock()
    style_2 = Style(int_prop=10)
    node.style = style_2

    # Style copies on assignment.
    assert isinstance(node.style, Style)
    assert node.style == style_2
    assert node.style is not style_2

    assert node.style != style_1

    # Since an applicator has already been assigned, assigning style applies the style.
    node.style.reapply.assert_called_once()


def test_assign_style_with_no_applicator():
    style_1 = Style(int_prop=5)
    node = Node(style=style_1)

    node.style.reapply.reset_mock()
    style_2 = Style(int_prop=10)
    node.style = style_2

    # Style copies on assignment.
    assert isinstance(node.style, Style)
    assert node.style == style_2
    assert node.style is not style_2

    assert node.style != style_1

    # Since no applicator was present, style should not be applied.
    node.style.reapply.assert_not_called()


def test_apply_before_node_is_ready():
    style = BrokenStyle()
    applicator = Mock()

    with pytest.warns(RuntimeWarning):
        node = Node(style=style)
        node.applicator = applicator

    with pytest.warns(RuntimeWarning):
        node.style = BrokenStyle()

    with pytest.warns(RuntimeWarning):
        Node(style=style, applicator=applicator)
