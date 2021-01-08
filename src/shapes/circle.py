import numpy as np
import math


class Circle:
    """
    Circle class, stores coords and style props.

    Attributes:
        x, y: center coords
        radius: circle radius
        fill_color: 3-int tuple representing rgb color
        stroke_color: 3-int tuple representing rgb color
        stroke_width: int representing stroke thickness
    """
    def __init__(self, x, y, radius, fill_color, stroke_color, stroke_width):
        """Constructor for Circle class.

        Args:
            x, y: center coords
            radius: circle radius
            fill_color: 3-int tuple representing rgb color
            stroke_color: 3-int tuple representing rgb color
            stroke_width: int representing stroke thickness
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width

    @staticmethod
    def from_svg_props(attrib, style):
        """Constructor for Circle class, takes svg props"""
        assert 'r' in attrib and 'cx' in attrib and 'cy' in attrib
        return Circle(float(attrib['cx']), float(attrib['cy']), float(attrib['r']), style[0], style[1], style[2])

    @staticmethod
    def _draw_disc(x, y, min_radius, max_radius, color, canvas):
        """Draws a disc with given props.

        Args:
            x, y: coords of 2d point
            min_radius, max_radius: disc dimensions
            color: 3-int tuple representing rgb color
            canvas: Canvas object
        Returns:
            None
        """
        for dx in np.arange(x - max_radius, x + max_radius, 1):
            for dy in np.arange(y - max_radius, y + max_radius, 1):
                if min_radius <= math.sqrt((dx - x) ** 2 + (dy - y) ** 2) < max_radius:
                    canvas.put_pixel(dx, dy, color)

    def draw_stroke(self, canvas):
        """Draws stroke-only circle"""
        if self.stroke_color:
            Circle._draw_disc(self.x, self.y,
                              self.radius - self.stroke_width / 2, self.radius + self.stroke_width / 2,
                              self.stroke_color, canvas)

    def draw_fill(self, canvas):
        """Draws filled circle"""
        if self.fill_color:
            Circle._draw_disc(self.x, self.y, 0, self.radius, self.fill_color, canvas)

    def draw(self, canvas):
        """Draws circle according to all svg attributes and props given in constructor"""
        self.draw_fill(canvas)
        self.draw_stroke(canvas)
