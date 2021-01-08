from src.shapes.line import Line


class Polyline:
    """
    Polyline class, stores a list of points and style properties.

    Attributes:
        points: a list of 2-int tuples representing 2d points
        color: 3-int tuple representing rgb color
        thickness: int representing line thickness
    """

    def __init__(self, points, color, thickness=2):
        """Constructor for Polyline class.

        Args:
            points: a list of 2-int tuples representing 2d points
            color: 3-int tuple representing rgb color
            thickness: int representing line thickness
        """
        self.points = points
        self.color = color
        self.thickness = thickness

    @staticmethod
    def parse_points(str_points):
        """Parses string from svg attribute and returns a list of 2d points"""
        points = []
        for str_point in str_points.split(' '):
            x, y = map(float, str_point.split(','))
            points.append((x, y))
        return points

    @staticmethod
    def from_svg_props(attrib, style):
        """Constructor for Polyline class, takes svg props"""
        return Polyline(Polyline.parse_points(attrib['points']), style[1], style[2])

    def draw(self, canvas):
        """Draws lines according to all props given in constructor"""
        for point_a, point_b in zip(self.points[:-1], self.points[1:]):
            Line(point_a[0], point_a[1], point_b[0], point_b[1], self.color, self.thickness).draw(canvas)
            print(point_a, point_b)
