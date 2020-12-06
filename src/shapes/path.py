import re
from src.shapes.line import Line


class Path:
    def __init__(self, steps, fill_color, stroke_color, stroke_width):
        self.steps = steps
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.cursor = None
        self.closure = None

    @staticmethod
    def from_svg_props(props):
        steps = re.findall(r'[A-Za-z][^A-Za-z]*', props.get('d', ''))
        return Path(steps, None, (165, 165, 255), 3)

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

    def consume_closure(self, step_type, step_data):
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
            'z': self.consume_closure
        }
        for step in self.steps:
            step_type, step_data = Path.parse_step(step)
            fun = func[step_type.lower()]
            object = fun(step_type, step_data)
            if object:
                # print(step_type, step_data)
                # print(self.cursor)
                object.draw(canvas)
