from src.canvas import Canvas
from src.shapes.rect import Rect
from src.shapes.circle import Circle


def main():
    canvas = Canvas(255, 255)
    rect = Rect(100, 50, 50, 100, (255, 255, 0), (255, 0, 255), 6)
    rect.draw(canvas)

    circle = Circle(50, 50, 20, (255, 255, 0), (255, 0, 255), 6)
    circle1 = Circle(150, 150, 20, (255, 255, 0), None, 6)
    circle2 = Circle(150, 130, 20, None, (255, 0, 255), 6)
    circle.draw(canvas)
    circle1.draw(canvas)
    circle2.draw(canvas)
    canvas.dump_to_png('test.png')


if __name__ == '__main__':
    main()
