from src.canvas import Canvas
from src.shapes.rect import Rect
from src.shapes.circle import Circle
from src.shapes.line import Line


def main():
    canvas = Canvas(255, 255)
    Rect(100, 50, 50, 100, (255, 255, 0), (255, 0, 255), 6).draw(canvas)
    Rect(200, 30, 30, 30, None, (255, 0, 255), 6).draw(canvas)

    Circle(50, 50, 20, (255, 255, 0), (255, 0, 255), 6).draw(canvas)
    Circle(150, 150, 20, (255, 255, 0), None, 6).draw(canvas)
    Circle(150, 130, 20, None, (255, 0, 255), 6).draw(canvas)

    Line(50, 125, 60, 200, (255, 255, 255), 3).draw(canvas)
    Line(65, 200, 150, 220, (255, 255, 255), 6).draw(canvas)

    canvas.dump_to_png('test.png')


if __name__ == '__main__':
    main()
