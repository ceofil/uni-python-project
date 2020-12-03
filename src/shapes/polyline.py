from src.shapes.line import Line


class Polyline:
    def __init__(self, points, color, thickness=2):
        self.points = points
        self.color = color
        self.thickness = thickness

    def draw(self, canvas):
        for point_a, point_b in zip(self.points[:-1], self.points[1:]):
            Line(point_a[0], point_a[1], point_b[0], point_b[1], self.color, self.thickness).draw(canvas)
            print(point_a, point_b)
