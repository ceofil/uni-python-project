from src.canvas import Canvas
from src.utils.xml_parser import parse_xml
from src.shapes.rect import Rect
from src.shapes.circle import Circle
from src.shapes.line import Line
from src.shapes.polyline import Polyline
from src.shapes.path import Path
from src.shapes.ellipse import Ellipse


def main():
    canvas = Canvas(500, 500)

    objects = parse_xml(r'D:\GitHub\uni-python-project\src\input\test.svg')
    for obj in objects:
        obj.draw(canvas)

    canvas.dump_to_png('test.png')


def interpolate(x1, y1, x2, y2, current_step, total_steps):
    dx1, dy1 = (x2 - x1) / total_steps, (y2 - y1) / total_steps
    mx1, my1 = x1 + dx1 * current_step, y1 + dy1 * current_step
    return mx1, my1


def three_points_bezier(x1, y1, x2, y2, x3, y3, canvas, color):
    steps = 1000

    points = []
    for idx in range(steps + 1):
        mx1, my1 = interpolate(x1, y1, x2, y2, idx, steps)
        mx2, my2 = interpolate(x2, y2, x3, y3, idx, steps)

        px, py = interpolate(mx1, my1, mx2, my2, idx, steps)
        points.append((px, py))

    for a, b in zip(points[:-1], points[1:]):
        lx1, ly1 = a
        lx2, ly2 = b
        Line(lx1, ly1, lx2, ly2, color, 4).draw(canvas)


def four_points_bezier(x1, y1, x2, y2, x3, y3, x4, y4, canvas, color):
    steps = 90
    points = []
    for idx in range(steps + 1):
        mx1, my1 = interpolate(x1, y1, x2, y2, idx, steps)
        mx2, my2 = interpolate(x2, y2, x3, y3, idx, steps)
        mx3, my3 = interpolate(x3, y3, x4, y4, idx, steps)

        px1, py1 = interpolate(mx1, my1, mx2, my2, idx, steps)
        px2, py2 = interpolate(mx2, my2, mx3, my3, idx, steps)

        qx, qy = interpolate(px1, py1, px2, py2, idx, steps)
        points.append((qx, qy))

    for a, b in zip(points[:-1], points[1:]):
        lx1, ly1 = a
        lx2, ly2 = b
        Line(lx1, ly1, lx2, ly2, color, 4).draw(canvas)


def test():
    canvas = Canvas(500, 500)

    x1, y1 = 100, 250
    x2, y2 = 250, 100
    x3, y3 = 250, 400
    x4, y4 = 400, 350
    Circle(x1, y1, 10, (255, 0, 0), None, None).draw(canvas)
    Circle(x2, y2, 10, (255, 0, 0), None, None).draw(canvas)
    Circle(x3, y3, 10, (255, 0, 0), None, None).draw(canvas)
    Circle(x4, y4, 10, (255, 0, 0), None, None).draw(canvas)
    Line(x1, y1, x2, y2, (255, 0, 0), 5).draw(canvas)
    Line(x3, y3, x2, y2, (255, 0, 0), 5).draw(canvas)
    Line(x3, y3, x4, y4, (255, 0, 0), 5).draw(canvas)

    three_points_bezier(x1, y1, x2, y2, x3, y3, canvas, (255, 0, 255))
    four_points_bezier(x1, y1, x2, y2, x3, y3, x4, y4, canvas, (0, 0, 255))
    canvas.dump_to_png('test.png')


if __name__ == '__main__':
    test()
