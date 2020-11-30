import xml.etree.ElementTree as ET

if __name__ == '__main__':
    path = r'D:\GitHub\uni-python-project\src\input\test.svg'
    tree = ET.parse(path)
    root = tree.getroot()
    for child in root:
        print(child.tag, child.attrib)
