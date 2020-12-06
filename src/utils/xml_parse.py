import xml.etree.ElementTree as ET
from src.shapes.path import Path


def draw_path():
    path = r'D:\GitHub\uni-python-project\src\input\path.svg'
    tree = ET.parse(path)
    root = tree.getroot()
    for child in root:
        if 'path' in child.tag:
            path = Path.from_svg_props(child.attrib)
            for step in path.steps:
                print(Path.parse_step(step))
