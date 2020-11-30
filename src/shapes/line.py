import numpy as np


class Line:
    def __init__(self, x0, y0, x1, y1, color, thickness=2):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.color = color
        self.thickness = thickness

    def draw(self, canvas):
        dx = abs(self.x1 - self.x0)
        dy = abs(self.y1 - self.y0)

        if dy > dx:
            m = dx / dy
            b = self.x0 - m * self.y0
            y_start, y_end = min(self.y0, self.y1), max(self.y0, self.y1)
            for y in np.arange(y_start, y_end, 1):
                x = m * y + b
                for tx in np.arange(x - self.thickness / 2, x + self.thickness / 2, 1):
                    canvas.put_pixel(tx, y, self.color)
        else:
            m = dy / dx
            b = self.y0 - m * self.x0
            x_start, x_end = min(self.x0, self.x1), max(self.x0, self.x1)

            for x in np.arange(x_start, x_end, 1):
                y = m * x + b
                for ty in np.arange(y - self.thickness / 2, y + self.thickness / 2, 1):
                    canvas.put_pixel(x, ty, self.color)
