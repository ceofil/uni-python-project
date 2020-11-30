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

    def draw_fill(self, canvas):
        if self.fill:
            Rect._draw_fill(self.x, self.y, self.width, self.height, self.fill, canvas)

    def draw_stroke(self, canvas):
        if self.stroke_color:
            Rect._draw_fill(
                self.x - self.stroke_width / 2, self.y - self.stroke_width / 2,
                self.width + self.stroke_width, self.stroke_width,
                self.stroke_color, canvas
            )
            Rect._draw_fill(
                self.x - self.stroke_width / 2, self.y + self.height - self.stroke_width / 2,
                self.width + self.stroke_width, self.stroke_width,
                self.stroke_color, canvas
            )
            Rect._draw_fill(
                self.x - self.stroke_width / 2, self.y - self.stroke_width / 2,
                self.stroke_width, self.height + self.stroke_width,
                self.stroke_color, canvas
            )
            Rect._draw_fill(
                self.x + self.width - self.stroke_width / 2, self.y - self.stroke_width / 2,
                self.stroke_width, self.height + self.stroke_width,
                self.stroke_color, canvas
            )

    def draw(self, canvas):
        self.draw_fill(canvas)
        self.draw_stroke(canvas)
