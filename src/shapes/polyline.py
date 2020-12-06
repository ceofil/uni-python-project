from src.shapes.line import Line


class Polyline:
    def __init__(self, points, color, thickness=2):
        self.points = points
        self.color = color
        self.thickness = thickness

    @staticmethod
    def parse_ponts(str_points):
        points = []
        for str_point in str_points.split(' '):
            x, y = map(float, str_point.split(','))
            points.append((x, y))
        return points

    @staticmethod
    def from_svg_props(attrib, style):
        return Polyline(Polyline.parse_ponts(attrib['points']), style[1], style[2])

    def draw(self, canvas):
        for point_a, point_b in zip(self.points[:-1], self.points[1:]):
            Line(point_a[0], point_a[1], point_b[0], point_b[1], self.color, self.thickness).draw(canvas)
            print(point_a, point_b)
