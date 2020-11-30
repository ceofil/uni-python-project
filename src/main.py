import png
from src.canvas import Canvas
from src.shapes.rect import Rect


def main():
    canvas = Canvas(255, 255)
    rect = Rect(100, 50, 50, 100, (255, 255, 0), (255, 0, 255), 6)
    rect.draw(canvas)
    canvas.dump_to_png('test.png')


if __name__ == '__main__':
    main()
