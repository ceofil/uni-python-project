import re
from src.shapes.line import Line
from src.shapes.ellipse import Ellipse
from src.shapes.circle import Circle
import numpy as np


class Path:
    def __init__(self, steps, fill_color, stroke_color, stroke_width):
        self.steps = steps
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.cursor = None
        self.closure = None

    @staticmethod
    def from_svg_props(props, style):
        steps = re.findall(r'[A-Za-z][^A-Za-z]*', props.get('d', ''))
        return Path(steps, style[0], style[1], style[2])

    @staticmethod
    def parse_step(step):
        step_type = step[0]
        assert step_type.lower() in 'mlhvcsqtaz'
        step = step[1:]
        points = []
        if not step_type.lower() == 'z':
            for point in step.split(','):
                points.append(tuple(map(float, point.strip().split(' '))))
        return step_type, points

    def consume_move(self, step_type, step_data):
        assert step_type.lower() == 'm'
        assert len(step_data) == 1, "invalid M step in path"
        self.cursor = step_data[0]
        self.closure = step_data[0]

    def consume_horizontal(self, step_type, step_data):
        assert step_type.lower() == 'h'
        print(step_data)
        assert len(step_data[0]) == 1, "invalid H/h step in path"
        x0, y0 = self.cursor
        x1, y1 = step_data[0][0], y0
        if step_type == 'h':
            x1 += x0
        self.cursor = (x1, y1)
        return Line(x0, y0, x1, y1, self.stroke_color, self.stroke_width)

    def consume_vertical(self, step_type, step_data):
        assert step_type.lower() == 'v'
        assert len(step_data[0]) == 1, "invalid V/v step in path"
        x0, y0 = self.cursor
        x1, y1 = x0, step_data[0][0]
        if step_type == 'v':
            y1 += y0
        self.cursor = (x1, y1)
        return Line(x0, y0, x1, y1, self.stroke_color, self.stroke_width)

    def consume_line(self, step_type, step_data):
        assert step_type.lower() == 'l'
        assert len(step_data[0]) == 2, "invalid L/l step in path"
        x0, y0 = self.cursor
        x1, y1 = step_data[0]
        if step_type == 'l':
            x1 += x0
            y1 += y0
        self.cursor = (x1, y1)
        return Line(x0, y0, x1, y1, self.stroke_color, self.stroke_width)

    def point_is_on_ellipse(self, x, y, cx, cy, rx, ry):
        threshhold = 1
        is_inside_small_ellipse = Ellipse.ellipse_factor(x, y, cx, cy, rx - threshhold, ry - threshhold) < 1
        is_inside_big_ellipse = Ellipse.ellipse_factor(x, y, cx, cy, rx + threshhold, ry + threshhold) < 1
        return is_inside_big_ellipse and not is_inside_small_ellipse

    def find_ellipse_centers(self, p1, p2, rx, ry, canvas):
        x0, y0 = p1
        x1, y1 = p2

        dx, dy = x1 - x0, y1 - y0

        centers = []
        for mx in np.arange(-rx, rx, 1):
            for my in np.arange(-ry, ry, 1):
                if self.point_is_on_ellipse(mx, my, 0, 0, rx, ry) and \
                        self.point_is_on_ellipse(mx + dx, my + dy, 0, 0, rx, ry):
                    cx0, cy0 = x0 - mx, y0 - my
                    centroid_x, centroid_y = (x0 + x1) / 2, (y0 + y1) / 2
                    cx1, cy1 = centroid_x + (centroid_x - cx0), centroid_y + (centroid_y - cy0)
                    centers = [(cx0, cy0), (cx1, cy1)]
                    break
        return centers

    def consume_arch(self, step_type, step_data, canvas):
        assert step_type.lower() == 'a'
        print(step_data, step_type)
        data = step_data[0]
        rx = data[0]
        ry = data[1]
        meta = data[3]
        x1 = data[4]
        y1 = data[5]
        x0, y0 = self.cursor
        if step_type == 'a':
            x1 += x0
            y1 += y0
        centers = self.find_ellipse_centers((x0, y0), (x1, y1), rx, ry, canvas)
        if centers:
            for cx, cy in centers:
                Ellipse(cx, cy, rx, ry, None, (0, 0, 255), 1).draw(canvas)
        return Line(x0, y0, x1, y1, (0, 0, 0), 2)

    def consume_closure(self, step_type, _):
        assert step_type.lower() == 'z'
        line = Line(self.cursor[0], self.cursor[1], self.closure[0], self.closure[1], self.stroke_color,
                    self.stroke_width)
        self.cursor = self.closure
        return line

    def draw(self, canvas):
        func = {
            'm': self.consume_move,
            'h': self.consume_horizontal,
            'v': self.consume_vertical,
            'l': self.consume_line,
            'a': self.consume_arch,
            'z': self.consume_closure
        }
        for step in self.steps:
            step_type, step_data = Path.parse_step(step)
            if step_type.lower() == 'a':
                object = self.consume_arch(step_type, step_data, canvas)
            else:
                fun = func[step_type.lower()]
                object = fun(step_type, step_data)
            if object:
                # print(step_type, step_data)
                # print(self.cursor)
                object.draw(canvas)
