import re
from src.shapes.line import Line
from src.shapes.ellipse import Ellipse
from src.utils.bezier_utils import three_points_bezier, four_points_bezier


class Path:
    """
    Path class, stores a list of svg-path steps, and style props.

    Attributes:
        steps: a list of svg-steps in string format representing a given instruction and a set of coords
        fill_color: 3-int tuple representing rgb color
        stroke_color: 3-int tuple representing rgb color
        stroke_width: int representing line thickness
        cursor: 2d point representing current position
        closure: 2d point representing starting position
        last_control_point: 2d point, last anchor for a bezier curve (used for smooth bezier curves)
    """

    def __init__(self, steps, fill_color, stroke_color, stroke_width):
        """Constructor for Path class.

        Args:
            steps: a list of svg-steps in string format representing a given instruction and a set of coords
            fill_color: 3-int tuple representing rgb color
            stroke_color: 3-int tuple representing rgb color
            stroke_width: int representing line thickness.
        """
        self.steps = steps
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.cursor = None
        self.closure = None
        self.last_control_point = None

    @staticmethod
    def from_svg_props(props, style):
        """Constructor for Path class, takes svg props."""
        steps = re.findall(r'[A-Za-z][^A-Za-z]*', props.get('d', ''))
        return Path(steps, style[0], style[1], style[2])

    @staticmethod
    def parse_step(step):
        """Takes svg-step in string format and returns instruction type and a list of points."""
        step_type = step[0]
        assert step_type.lower() in 'mlhvcsqtaz'
        step = step[1:]
        points = []
        if not step_type.lower() == 'z':
            for point in step.split(','):
                points.append(tuple(map(float, point.strip().split(' '))))
        return step_type, points

    def consume_move(self, step_type, step_data, _):
        """Moves cursor to given coords."""
        assert step_type.lower() == 'm'
        assert len(step_data) == 1, "invalid M step in path"
        self.cursor = step_data[0]
        self.closure = step_data[0]
        self.last_control_point = self.cursor

    def consume_horizontal(self, step_type, step_data, canvas):
        """Draws horizontal line and moves cursor to the end of the line."""
        assert step_type.lower() == 'h'
        print(step_data)
        assert len(step_data[0]) == 1, "invalid H/h step in path"
        x0, y0 = self.cursor
        x1, y1 = step_data[0][0], y0
        if step_type == 'h':
            x1 += x0
        self.cursor = (x1, y1)
        Line(x0, y0, x1, y1, self.stroke_color, self.stroke_width).draw(canvas)
        self.last_control_point = self.cursor

    def consume_vertical(self, step_type, step_data, canvas):
        """Draws vertical line and moves cursor to the end of the line."""
        assert step_type.lower() == 'v'
        assert len(step_data[0]) == 1, "invalid V/v step in path"
        x0, y0 = self.cursor
        x1, y1 = x0, step_data[0][0]
        if step_type == 'v':
            y1 += y0
        self.cursor = (x1, y1)
        Line(x0, y0, x1, y1, self.stroke_color, self.stroke_width).draw(canvas)
        self.last_control_point = self.cursor

    def consume_line(self, step_type, step_data, canvas):
        """Draws line and moves cursor to the end of the line."""
        assert step_type.lower() == 'l'
        assert len(step_data[0]) == 2, "invalid L/l step in path"
        x0, y0 = self.cursor
        x1, y1 = step_data[0]
        if step_type == 'l':
            x1 += x0
            y1 += y0
        self.cursor = (x1, y1)
        Line(x0, y0, x1, y1, self.stroke_color, self.stroke_width).draw(canvas)
        self.last_control_point = self.cursor

    def consume_arch(self, step_type, step_data, canvas):
        """Draws arch and moves cursor to the end of the arch, updates last control point."""
        assert step_type.lower() == 'a'
        data = step_data[0]
        rx = data[0]
        ry = data[1]
        upper = data[3]
        bigger = data[4]
        x1 = data[5]
        y1 = data[6]
        x0, y0 = self.cursor
        if step_type == 'a':
            x1 += x0
            y1 += y0
        centers = Ellipse.find_ellipse_centers((x0, y0), (x1, y1), rx, ry)

        if centers:
            centers.sort(key=lambda c: c[1])  # sorting the points by Y, the one on the top will be first
            # this if-else can probably be simplified with xor or some binary operation
            if upper:
                center_idx = 0 if bigger else 1
            else:
                center_idx = 1 if bigger else 0
            cx, cy = centers[center_idx]
            self.cursor = (x1, y1)
            Ellipse(cx, cy, rx, ry, self.fill_color, self.stroke_color, self.stroke_width,
                    below_line=(not upper, ((x0, y0), (x1, y1)))).draw(canvas)
        self.last_control_point = self.cursor

    def consume_cubic_bezier_curve(self, step_type, step_data, canvas):
        """Draws cubic bezier and moves cursor to the end of the curve, updates last control point."""
        assert step_type.lower() == 'c'
        x0, y0 = self.cursor
        (x_handle0, y_handle0), (x_handle1, y_handle1), (x1, y1) = step_data
        if step_type == 'c':
            (x_handle0, y_handle0), (x_handle1, y_handle1), (x1, y1) = \
                (x_handle0 + x0, y_handle0 + y0), (x_handle1 + x0, y_handle1 + y0), (x1 + x0, y1 + y0)
        four_points_bezier(x0, y0, x_handle0, y_handle0, x_handle1, y_handle1, x1, y1, canvas, self.stroke_color,
                           self.stroke_width)
        self.cursor = (x1, y1)
        self.last_control_point = x_handle1, y_handle1

    def consume_smooth_cubic_bezier_curve(self, step_type, step_data, canvas):
        """Draws smooth cubic bezier and moves cursor to the end of the curve, updates last control point."""
        assert step_type.lower() == 's'
        if self.last_control_point is None:
            self.last_control_point = self.cursor
        x_last_handle, y_last_handle = self.last_control_point
        x0, y0 = self.cursor
        x_handle0, y_handle0 = x0 + (x0 - x_last_handle), y0 + (y0 - y_last_handle)

        x_handle1, y_handle1 = step_data[0]
        x1, y1 = step_data[1]
        if step_type == 's':
            x1, y1, x_handle1, y_handle1 = x1 + x0, y1 + y0, x_handle1 + x0, y_handle1 + y0
        four_points_bezier(x0, y0, x_handle0, y_handle0, x_handle1, y_handle1, x1, y1, canvas, self.stroke_color,
                           self.stroke_width)
        self.last_control_point = x_handle1, y_handle1

    def consume_quadratic_bezier_curve(self, step_type, step_data, canvas):
        """Draws quadratic bezier and moves cursor to the end of the curve, updates last control point."""
        assert step_type.lower() == 'q'
        x0, y0 = self.cursor
        if len(step_data[0]) == 4:
            anchor_x, anchor_y, x1, y1 = step_data[0]
        else:
            (anchor_x, anchor_y), (x1, y1) = step_data[0]
        if step_type == 'q':
            x1, y1 = x1 + x0, y1 + y0
            anchor_x, anchor_y = anchor_x + x0, anchor_y + y0
        three_points_bezier(x0, y0, anchor_x, anchor_y, x1, y1, canvas, self.stroke_color, self.stroke_width)
        self.cursor = (x1, y1)
        self.last_control_point = anchor_x, anchor_y

    def consume_smooth_quadratic_bezier_curve(self, step_type, step_data, canvas):
        """Draws smooth quadratic bezier and moves cursor to the end of the curve, updates last control point."""
        assert step_type.lower() == 't'
        x1, y1 = step_data[0]
        if self.last_control_point is None:
            self.last_control_point = self.cursor
        x_last_handle, y_last_handle = self.last_control_point
        x0, y0 = self.cursor
        x_handle0, y_handle0 = x0 + (x0 - x_last_handle), y0 + (y0 - y_last_handle)
        if step_type == 't':
            x1, y1 = x1 + x0, y1 + y0
            x_handle0, y_handle0 = x_handle0 + x0, y_handle0 + y0
        three_points_bezier(x0, y0, x_handle0, y_handle0, x1, y1, canvas, self.stroke_color, self.stroke_width)
        self.last_control_point = x_handle0, y_handle0
        self.cursor = (x1, y1)

    def consume_closure(self, step_type, _, canvas):
        """Moves cursor ath the starting point"""
        assert step_type.lower() == 'z'
        Line(self.cursor[0], self.cursor[1], self.closure[0], self.closure[1], self.stroke_color,
             self.stroke_width).draw(canvas)
        self.cursor = self.closure
        self.last_control_point = self.cursor

    def draw(self, canvas):
        """Draw svg path according to all style props and path-steps given in the constructor"""
        step_type_to_function_map = {
            'm': self.consume_move,
            'h': self.consume_horizontal,
            'v': self.consume_vertical,
            'l': self.consume_line,
            'a': self.consume_arch,
            'c': self.consume_cubic_bezier_curve,
            's': self.consume_smooth_cubic_bezier_curve,
            'q': self.consume_quadratic_bezier_curve,
            't': self.consume_smooth_quadratic_bezier_curve,
            'z': self.consume_closure
        }
        for step in self.steps:
            step_type, step_data = Path.parse_step(step)
            if step_type.lower() in step_type_to_function_map:
                fun = step_type_to_function_map[step_type.lower()]
                fun(step_type, step_data, canvas)
