from src.shapes.line import Line


class Rect:
    """
    Rect class, stores boundries and dimensions of given rectangle.

    Attributes:
        x, y: float on-screen coords (left, top)
        width, height: dimensions of the rectangle
        fill: 3-int tuple, rgb color (fill_color)
        stroke_color: 3-int tuple, rgb color
        stroke_width: int representing stroke thickness
    """
    def __init__(self, x, y, width, height, fill, stroke_color, stroke_width):
        """Constructor for Rect class.

        Args:
            x, y: float on-screen coords (left, top)
            width, height: dimensions of the rectangle
            fill: 3-int tuple, rgb color (fill_color)
            stroke_color: 3-int tuple, rgb color
            stroke_width: int representing stroke thickness
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill = fill
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width

    @staticmethod
    def from_svg_props(attrib, style):
        """Constructor for Rect class.

        Args:
            attrib: parsed attributes from xml component
            style: parsed style from xml component
        """
        return Rect(float(attrib['x']), float(attrib['y']), float(attrib['width']), float(attrib['height']), style[0],
                    style[1], style[2])

    @staticmethod
    def _draw_fill(x, y, width, height, color, canvas):
        """Draws a filled rectangle at given coords.

        Args:
            x, y: on screen left-top coords
            width, height: dimensions of the rectangle
            color: 3-int tuple representing rgb color
            canvas: Canvas object
        Returns:
            None
        """
        x, y, width, height = int(x), int(y), int(width), int(height)
        for dx in range(x, x + width):
            for dy in range(y, y + height):
                canvas.put_pixel(dx, dy, color)

    @staticmethod
    def _draw_fill_from_center(x, y, width, height, color, canvas):
        """Draws a filled rectangle at given coords.

        Args:
            x, y: on screen coords (center of the rectangle)
            width, height: dimensions of the rectangle
            color: 3-int tuple representing rgb color
            canvas: Canvas object
        Returns:
            None
        """
        Rect._draw_fill(x - width / 2, y - height / 2, width, height, color, canvas)

    def draw_fill(self, canvas):
        """Draws a filled rectangle at coords initialized in constructor."""
        if self.fill:
            Rect._draw_fill(self.x, self.y, self.width, self.height, self.fill, canvas)

    def draw_stroke(self, canvas):
        """Draws a stroke-only rectangle at coords initialized in constructor."""
        if self.stroke_color:
            Line(self.x, self.y, self.x + self.width, self.y, self.stroke_color, self.stroke_width).draw(canvas)
            Line(self.x, self.y + self.height, self.x + self.width, self.y + self.height, self.stroke_color,
                 self.stroke_width).draw(canvas)
            Line(self.x, self.y, self.x, self.y + self.height, self.stroke_color, self.stroke_width).draw(canvas)
            Line(self.x + self.width, self.y, self.x + self.width, self.y + self.height, self.stroke_color,
                 self.stroke_width).draw(canvas)

            Rect._draw_fill_from_center(self.x, self.y, self.stroke_width, self.stroke_width, self.stroke_color, canvas)
            Rect._draw_fill_from_center(self.x + self.width, self.y, self.stroke_width, self.stroke_width,
                                        self.stroke_color, canvas)
            Rect._draw_fill_from_center(self.x, self.y + self.height, self.stroke_width, self.stroke_width,
                                        self.stroke_color, canvas)
            Rect._draw_fill_from_center(self.x + self.width, self.y + self.height, self.stroke_width, self.stroke_width,
                                        self.stroke_color, canvas)

    def draw(self, canvas):
        """Draws rectangle accrdoing to all properties given in the constructor."""
        self.draw_fill(canvas)
        self.draw_stroke(canvas)
