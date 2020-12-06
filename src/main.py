from src.canvas import Canvas
from src.utils.xml_parser import parse_xml


def main():
    canvas = Canvas(500, 500)

    objects = parse_xml(r'D:\GitHub\uni-python-project\src\input\test.svg')
    for obj in objects:
        obj.draw(canvas)

    canvas.dump_to_png('test.png')


if __name__ == '__main__':
    main()
