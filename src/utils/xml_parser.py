import xml.etree.ElementTree as ET
from src.shapes.rect import Rect
from src.shapes.circle import Circle
from src.shapes.line import Line
from src.shapes.polyline import Polyline
from src.shapes.path import Path
import re


def convert_color(clr):
    if clr:
        match = re.search(r'rgb\((\d+),(\d+),(\d+)\)', clr)
        if match:
            r, g, b = match.groups()
            return int(r), int(g), int(b)

    colors = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'pink': (255, 165, 165),
        'orange': (255, 165, 0),
        'magenta': (255, 0, 255),
        'yellow': (0, 255, 255),
        'brown': (165, 50, 50),
        'gray': (165, 165, 165)
    }
    if clr and clr.lower() in colors:
        return colors[clr.lower()]

    return None


def parse_style(attrib):
    fill_color = None
    stroke_color = None
    stroke_width = None
    if 'style' in attrib:
        style = dict()
        style_str = attrib['style']
        for pair in style_str.split(';'):
            key, value = pair.split(':')
            style[key] = value
        fill_color = style.get('fill', fill_color)
        stroke_color = style.get('stroke', stroke_color)
        stroke_width = style.get('stroke-width', stroke_width)
    fill_color = attrib.get('fill', fill_color)
    stroke_color = attrib.get('stroke', stroke_color)
    stroke_width = attrib.get('stroke-width', stroke_width)

    fill_color = convert_color(fill_color)
    stroke_color = convert_color(stroke_color)
    if stroke_color and not stroke_width:
        stroke_width = 1
    if stroke_width:
        stroke_width = float(stroke_width)
    return fill_color, stroke_color, stroke_width


def parse_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    shapes = {
        'circle': Circle,
        'line': Line,
        'path': Path,
        'polyline': Polyline,
        'rect': Rect
    }

    objects = []
    for child in root:
        style = parse_style(child.attrib)
        tag = child.tag.split('}')[1]
        if tag in shapes:
            shape_class = shapes[tag]
            objects.append(shape_class.from_svg_props(child.attrib, style))
    return objects


if __name__ == '__main__':
    print(parse_xml(r'D:\GitHub\uni-python-project\src\input\test.svg'))
