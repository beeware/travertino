from unittest import TestCase

from travertino.declaration import BaseStyle
from travertino.layout import BaseBox, Viewport
from travertino.node import Node
from travertino.size import BaseIntrinsicSize


class Style(BaseStyle):
    class IntrinsicSize(BaseIntrinsicSize):
        pass

    class Box(BaseBox):
        pass

    def layout(self, root, viewport):
        # A simple layout scheme that allocats twice the viewport size.
        root.layout.content_width = viewport.width * 2
        root.layout.content_height = viewport.height * 2


class ViewportTests(TestCase):
    def test_default(self):
        viewport = Viewport()

        self.assertEqual(viewport.width, 0)
        self.assertEqual(viewport.height, 0)
        self.assertEqual(viewport.dpi, None)

    def test_constructor(self):
        viewport = Viewport(width=640, height=480, dpi=96)

        self.assertEqual(viewport.width, 640)
        self.assertEqual(viewport.height, 480)
        self.assertEqual(viewport.dpi, 96)


class BoxTests(TestCase):
    def setUp(self):
        self.maxDiff = None

        self.grandchild1_1 = Node(style=Style())
        self.grandchild1_1.layout.content_width = 10
        self.grandchild1_1.layout.content_height = 16
        self.grandchild1_2 = Node(style=Style())

        self.child1 = Node(
            style=Style(), children=[self.grandchild1_1, self.grandchild1_2]
        )
        self.child1.layout.content_width = 10
        self.child1.layout.content_height = 16
        self.child2 = Node(style=Style(), children=[])

        self.node = Node(style=Style(), children=[self.child1, self.child2])
        self.node.layout.content_width = 10
        self.node.layout.content_height = 16

    def assertLayout(self, box, expected):
        actual = {
            "origin": (box._origin_left, box._origin_top),
            "size": (box.width, box.height),
            "content": (box.content_width, box.content_height),
            "relative": (
                box.content_top,
                box.content_right,
                box.content_bottom,
                box.content_left,
            ),
            "absolute": (
                box.absolute_content_top,
                box.absolute_content_right,
                box.absolute_content_bottom,
                box.absolute_content_left,
            ),
        }
        self.assertEqual(actual, expected)

    def test_repr(self):
        self.node.layout._origin_top = 1
        self.node.layout._origin_left = 2
        self.assertEqual(repr(self.node.layout), "<Box (10x16 @ 2,1)>")

    def test_initial(self):
        # Core attributes have been stored
        self.assertLayout(
            self.node.layout,
            {
                "origin": (0, 0),
                "size": (10, 16),
                "content": (10, 16),
                "relative": (0, 0, 0, 0),
                "absolute": (0, 10, 16, 0),
            },
        )

    def test_set_content_top(self):
        self.node.layout.content_top = 5

        self.assertLayout(
            self.node.layout,
            {
                "origin": (0, 0),
                "size": (10, 21),
                "content": (10, 16),
                "relative": (5, 0, 0, 0),
                "absolute": (5, 10, 21, 0),
            },
        )

        # Set the top to a new value
        self.node.layout.content_top = 7

        self.assertLayout(
            self.node.layout,
            {
                "origin": (0, 0),
                "size": (10, 23),
                "content": (10, 16),
                "relative": (7, 0, 0, 0),
                "absolute": (7, 10, 23, 0),
            },
        )

    def test_set_content_left(self):
        self.node.layout.content_left = 5

        self.assertLayout(
            self.node.layout,
            {
                "origin": (0, 0),
                "size": (15, 16),
                "content": (10, 16),
                "relative": (0, 0, 0, 5),
                "absolute": (0, 15, 16, 5),
            },
        )

        # Set the left to a new value
        self.node.layout.content_left = 7

        self.assertLayout(
            self.node.layout,
            {
                "origin": (0, 0),
                "size": (17, 16),
                "content": (10, 16),
                "relative": (0, 0, 0, 7),
                "absolute": (0, 17, 16, 7),
            },
        )

    def test_set_content_width(self):
        self.node.layout.content_width = 5

        self.assertLayout(
            self.node.layout,
            {
                "origin": (0, 0),
                "size": (5, 16),
                "content": (5, 16),
                "relative": (0, 0, 0, 0),
                "absolute": (0, 5, 16, 0),
            },
        )

        # Set the width to a new value
        self.node.layout.content_width = 7

        self.assertLayout(
            self.node.layout,
            {
                "origin": (0, 0),
                "size": (7, 16),
                "content": (7, 16),
                "relative": (0, 0, 0, 0),
                "absolute": (0, 7, 16, 0),
            },
        )

    def test_set_content_height(self):
        self.node.layout.content_height = 5

        self.assertLayout(
            self.node.layout,
            {
                "origin": (0, 0),
                "size": (10, 5),
                "content": (10, 5),
                "relative": (0, 0, 0, 0),
                "absolute": (0, 10, 5, 0),
            },
        )

        # Set the height to a new value
        self.node.layout.content_height = 7

        self.assertLayout(
            self.node.layout,
            {
                "origin": (0, 0),
                "size": (10, 7),
                "content": (10, 7),
                "relative": (0, 0, 0, 0),
                "absolute": (0, 10, 7, 0),
            },
        )

    def test_descendent_offsets(self):
        self.node.layout.content_top = 7
        self.node.layout.content_left = 8

        self.child1.layout.content_top = 9
        self.child1.layout.content_left = 10

        self.grandchild1_1.layout.content_top = 11
        self.grandchild1_1.layout.content_left = 12

        self.assertLayout(
            self.node.layout,
            {
                "origin": (0, 0),
                "size": (18, 23),
                "content": (10, 16),
                "relative": (7, 0, 0, 8),
                "absolute": (7, 18, 23, 8),
            },
        )

        self.assertLayout(
            self.child1.layout,
            {
                "origin": (8, 7),
                "size": (20, 25),
                "content": (10, 16),
                "relative": (9, 0, 0, 10),
                "absolute": (16, 28, 32, 18),
            },
        )

        self.assertLayout(
            self.grandchild1_1.layout,
            {
                "origin": (18, 16),
                "size": (22, 27),
                "content": (10, 16),
                "relative": (11, 0, 0, 12),
                "absolute": (27, 40, 43, 30),
            },
        )

        # Modify the grandchild position
        self.grandchild1_1.layout.content_top = 13
        self.grandchild1_1.layout.content_left = 14

        # Only the grandchild position has changed.
        self.assertLayout(
            self.node.layout,
            {
                "origin": (0, 0),
                "size": (18, 23),
                "content": (10, 16),
                "relative": (7, 0, 0, 8),
                "absolute": (7, 18, 23, 8),
            },
        )

        self.assertLayout(
            self.child1.layout,
            {
                "origin": (8, 7),
                "size": (20, 25),
                "content": (10, 16),
                "relative": (9, 0, 0, 10),
                "absolute": (16, 28, 32, 18),
            },
        )

        self.assertLayout(
            self.grandchild1_1.layout,
            {
                "origin": (18, 16),
                "size": (24, 29),
                "content": (10, 16),
                "relative": (13, 0, 0, 14),
                "absolute": (29, 42, 45, 32),
            },
        )

        # Modify the child position
        self.child1.layout.content_top = 15
        self.child1.layout.content_left = 16

        # The child and grandchild position has changed.
        self.assertLayout(
            self.node.layout,
            {
                "origin": (0, 0),
                "size": (18, 23),
                "content": (10, 16),
                "relative": (7, 0, 0, 8),
                "absolute": (7, 18, 23, 8),
            },
        )

        self.assertLayout(
            self.child1.layout,
            {
                "origin": (8, 7),
                "size": (26, 31),
                "content": (10, 16),
                "relative": (15, 0, 0, 16),
                "absolute": (22, 34, 38, 24),
            },
        )

        self.assertLayout(
            self.grandchild1_1.layout,
            {
                "origin": (24, 22),
                "size": (24, 29),
                "content": (10, 16),
                "relative": (13, 0, 0, 14),
                "absolute": (35, 48, 51, 38),
            },
        )

    def test_absolute_equalities(self):
        # Move the box around and set some borders.
        self.node.layout.origin_top = 100
        self.node.layout.origin_left = 200

        self.node.layout.content_top = 50
        self.node.layout.content_left = 75
        self.node.layout.content_right = 42
        self.node.layout.content_bottom = 37

        self.assertEqual(
            self.node.layout.absolute_content_left + self.node.layout.content_width,
            self.node.layout.absolute_content_right,
        )
        self.assertEqual(
            self.node.layout.absolute_content_top + self.node.layout.content_height,
            self.node.layout.absolute_content_bottom,
        )

        self.assertEqual(
            self.node.layout.content_left
            + self.node.layout.content_width
            + self.node.layout.content_right,
            self.node.layout.width,
        )
        self.assertEqual(
            self.node.layout.content_top
            + self.node.layout.content_height
            + self.node.layout.content_bottom,
            self.node.layout.height,
        )
