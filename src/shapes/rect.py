from src.shapes.line import Line


class Rect:
    def __init__(self, x, y, width, height, fill, stroke_color, stroke_width=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill = fill
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width if stroke_width is not None and stroke_color is not None else min(width,
                                                                                                           height) / 10

    @staticmethod
    def _draw_fill(x, y, width, height, color, canvas):
        x, y, width, height = int(x), int(y), int(width), int(height)
        for dx in range(x, x + width):
            for dy in range(y, y + height):
                canvas.put_pixel(dx, dy, color)

    @staticmethod
    def _draw_fill_from_center(x, y, width, height, color, canvas):
        Rect._draw_fill(x - width / 2, y - height / 2, width, height, color, canvas)

    def draw_fill(self, canvas):
        if self.fill:
            Rect._draw_fill(self.x, self.y, self.width, self.height, self.fill, canvas)

    def draw_stroke(self, canvas):
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
        self.draw_fill(canvas)
        self.draw_stroke(canvas)
