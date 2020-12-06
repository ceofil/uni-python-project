from src.canvas import Canvas
from src.shapes.rect import Rect
from src.shapes.circle import Circle
from src.shapes.line import Line
from src.shapes.polyline import Polyline
from src.shapes.path import Path
import xml.etree.ElementTree as ET


def test_draw_path(canvas):
    path = r'D:\GitHub\uni-python-project\src\input\path.svg'
    tree = ET.parse(path)
    root = tree.getroot()
    for child in root:
        if 'path' in child.tag:
            path = Path.from_svg_props(child.attrib)
            path.draw(canvas)


def main():
    canvas = Canvas(255, 255)
    Rect(0, 0, 255, 255, None, (255, 255, 255), 3).draw(canvas)
    Rect(100, 50, 50, 100, (255, 255, 0), (255, 0, 255), 6).draw(canvas)
    Rect(200, 30, 30, 30, None, (255, 0, 255), 6).draw(canvas)

    Circle(50, 50, 20, (255, 255, 0), (255, 0, 255), 6).draw(canvas)
    Circle(150, 150, 20, (255, 255, 0), None, 6).draw(canvas)
    Circle(150, 130, 20, None, (255, 0, 255), 6).draw(canvas)

    Line(50, 125, 60, 200, (0, 0, 255), 3).draw(canvas)
    Line(65, 200, 150, 220, (255, 0, 0), 6).draw(canvas)

    Polyline([(0, 0), (20, 240), (230, 230), (30, 230), (50, 50)], (0, 255, 0), 3).draw(canvas)
    test_draw_path(canvas)
    canvas.dump_to_png('test.png')


if __name__ == '__main__':
    main()
