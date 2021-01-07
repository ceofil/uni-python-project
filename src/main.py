from src.canvas import Canvas
from src.utils.xml_parser import parse_xml
from src.shapes.rect import Rect
from src.shapes.circle import Circle
from src.shapes.line import Line
from src.shapes.polyline import Polyline
from src.shapes.path import Path
from src.shapes.ellipse import Ellipse
from src.utils.bezier_utils import three_points_bezier, four_points_bezier

def main():
    canvas = Canvas(500, 500)
    Rect(0, 0, 500, 500, None, (255, 255, 255), 6).draw(canvas)

    objects = parse_xml(r'D:\GitHub\uni-python-project\src\input\path_c.svg')
    for obj in objects:
        obj.draw(canvas)

    canvas.dump_to_png('test.png')




def test():
    canvas = Canvas(500, 500)

    x1, y1 = 100, 250
    x2, y2 = 250, 100
    x3, y3 = 100, 400
    x4, y4 = 400, 350
    Circle(x1, y1, 10, (255, 0, 0), None, None).draw(canvas)
    Circle(x2, y2, 10, (255, 0, 255), None, None).draw(canvas)
    Circle(x3, y3, 10, (255, 0, 0), None, None).draw(canvas)
    Circle(x4, y4, 10, (255, 0, 255), None, None).draw(canvas)
    Rect(0, 0, 500, 500, None, (255, 255, 255), 3).draw(canvas)
    Line(x1, y1, x2, y2, (255, 0, 0), 5).draw(canvas)
    # Line(x3, y3, x2, y2, (255, 0, 0), 5).draw(canvas)
    Line(x3, y3, x4, y4, (255, 0, 0), 5).draw(canvas)
    #
    # three_points_bezier(x1, y1, x2, y2, x3, y3, canvas, (255, 0, 255))
    four_points_bezier(x2, y2, x1, y1, x3, y3, x4, y4, canvas, (0, 0, 255))
    canvas.dump_to_png('test.png')


if __name__ == '__main__':
    main()
