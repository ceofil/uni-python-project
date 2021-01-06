import math
import numpy as np


class Ellipse:
    def __init__(self, x, y, rx, ry, fill_color, stroke_color, stroke_width, below_line=(None, ((None, None), (None, None)))):
        self.x = x
        self.y = y
        self.rx = rx
        self.ry = ry
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.below, self.line = below_line

    @staticmethod
    def from_svg_props(attrib, style):
        return Ellipse(float(attrib['cx']), float(attrib['cy']), float(attrib['rx']), float(attrib['ry']), style[0],
                       style[1], style[2])

    @staticmethod
    def ellipse_factor(x, y, cx, cy, rx, ry):
        return ((cx - x) ** 2) / (rx ** 2) + ((cy - y) ** 2) / (ry ** 2)

    def points_is_below_line(self, point, a, b):
        center_x, center_y = a
        prime_x, prime_y = b
        mouse_x, mouse_y = point
        dx = prime_x - center_x
        dy = prime_y - center_y
        mx = mouse_x - center_x
        my = mouse_y - center_y
        cross = dx * my - dy * mx
        below = (cross > 0)
        if dx != 0:
            if dy / dx < 0:
                below = not below
        return below

    @staticmethod
    def point_is_on_ellipse(x, y, cx, cy, rx, ry):
        threshhold = 1
        is_inside_small_ellipse = Ellipse.ellipse_factor(x, y, cx, cy, rx - threshhold, ry - threshhold) < 1
        is_inside_big_ellipse = Ellipse.ellipse_factor(x, y, cx, cy, rx + threshhold, ry + threshhold) < 1
        return is_inside_big_ellipse and not is_inside_small_ellipse

    @staticmethod
    def find_ellipse_centers(p1, p2, rx, ry):
        x0, y0 = p1
        x1, y1 = p2

        dx, dy = x1 - x0, y1 - y0

        centers = []
        for mx in np.arange(-rx, rx, 1):
            for my in np.arange(-ry, ry, 1):
                if Ellipse.point_is_on_ellipse(mx, my, 0, 0, rx, ry) and \
                        Ellipse.point_is_on_ellipse(mx + dx, my + dy, 0, 0, rx, ry):
                    cx0, cy0 = x0 - mx, y0 - my
                    centroid_x, centroid_y = (x0 + x1) / 2, (y0 + y1) / 2
                    cx1, cy1 = centroid_x + (centroid_x - cx0), centroid_y + (centroid_y - cy0)
                    centers = [(cx0, cy0), (cx1, cy1)]
                    break
        return centers

    def draw(self, canvas):
        below, (a, b) = self.below, self.line
        for dx in np.arange(self.x - self.rx, self.x + self.rx, 1):
            for dy in np.arange(self.y - self.ry, self.y + self.ry, 1):
                if below is None:
                    line_check = True
                else:
                    line_check = below == self.points_is_below_line((dx, dy), a, b)

                if line_check:
                    inside_main_ellipse = Ellipse.ellipse_factor(
                        dx, dy, self.x, self.y,
                        self.rx - self.stroke_width,
                        self.ry - self.stroke_width) < 1
                    inside_extended_ellipse = Ellipse.ellipse_factor(
                        dx, dy, self.x, self.y, self.rx, self.ry) < 1
                    if inside_extended_ellipse:
                        if not inside_main_ellipse:
                            if self.stroke_color and self.stroke_width:
                                canvas.put_pixel(dx, dy, self.stroke_color)
                        elif self.fill_color:
                            canvas.put_pixel(dx, dy, self.fill_color)
