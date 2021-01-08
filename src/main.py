import os
from src.canvas import Canvas
from src.utils.xml_parser import parse_xml
import sys


def main():
    DEV = True
    if DEV:
        filename = r'D:\GitHub\uni-python-project\src\input\path_c.svg'
        output_name = 'test.png'
    else:
        filename = sys.argv[1]
        output_name = os.path.basename(filename).split('.')[0] + '.png'

    objects, view_box = parse_xml(filename)
    canvas = Canvas(view_box)
    for obj in objects:
        obj.draw(canvas)

    canvas.dump_to_png(output_name)


if __name__ == '__main__':
    main()
