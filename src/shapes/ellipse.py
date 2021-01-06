import math
import numpy as np


class Ellipse:
    def __init__(self, x, y, rx, ry, fill_color, stroke_color, stroke_width):
        self.x = x
        self.y = y
        self.rx = rx
        self.ry = ry
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width

    @staticmethod
    def from_svg_props(attrib, style):
        return Ellipse(float(attrib['cx']), float(attrib['cy']), float(attrib['rx']), float(attrib['ry']), style[0],
                       style[1], style[2])

    @staticmethod
    def _ellipse_factor(x, y, cx, cy, rx, ry):
        return ((cx - x) ** 2) / (rx ** 2) + ((cy - y) ** 2) / (ry ** 2)

    def draw(self, canvas):
        for dx in np.arange(self.x - self.rx, self.x + self.rx, 1):
            for dy in np.arange(self.y - self.ry, self.y + self.ry, 1):
                if Ellipse._ellipse_factor(dx, dy, self.x, self.y, self.rx, self.ry):
                    if self.stroke_color and self.stroke_width:
                        inside_main_ellipse = Ellipse._ellipse_factor(
                            dx, dy, self.x, self.y,
                            self.rx - self.stroke_width,
                            self.ry - self.stroke_width) < 1
                        inside_extened_ellipse = Ellipse._ellipse_factor(
                            dx, dy, self.x, self.y,self.rx, self.ry) < 1
                        if inside_extened_ellipse:
                            if not inside_main_ellipse:
                                canvas.put_pixel(dx, dy, self.stroke_color)
                            else:
                                canvas.put_pixel(dx, dy, self.fill_color)