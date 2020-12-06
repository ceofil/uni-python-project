import numpy as np
import math


class Circle:
    def __init__(self, x, y, radius, fill_color, stroke_color, stroke_width):
        self.x = x
        self.y = y
        self.radius = radius
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width

    @staticmethod
    def from_svg_props(attrib, style):
        assert 'r' in attrib and 'cx' in attrib and 'cy' in attrib
        return Circle(float(attrib['cx']), float(attrib['cy']), float(attrib['r']), style[0], style[1], style[2])

    @staticmethod
    def _draw_disc(x, y, min_radius, max_radius, color, canvas):
        for dx in np.arange(x - max_radius, x + max_radius, 1):
            for dy in np.arange(y - max_radius, y + max_radius, 1):
                if min_radius <= math.sqrt((dx - x) ** 2 + (dy - y) ** 2) < max_radius:
                    canvas.put_pixel(dx, dy, color)

    def draw_stroke(self, canvas):
        if self.stroke_color:
            Circle._draw_disc(self.x, self.y,
                              self.radius - self.stroke_width / 2, self.radius + self.stroke_width / 2,
                              self.stroke_color, canvas)

    def draw_fill(self, canvas):
        if self.fill_color:
            Circle._draw_disc(self.x, self.y, 0, self.radius, self.fill_color, canvas)

    def draw(self, canvas):
        self.draw_fill(canvas)
        self.draw_stroke(canvas)
