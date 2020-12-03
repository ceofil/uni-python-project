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
        dx = self.x1 - self.x0
        dy = self.y1 - self.y0

        if abs(dy) > abs(dx):
            m = dx / dy
            b = self.x0 - m * self.y0
            step = 1 if self.y0 < self.y1 else -1
            for y in np.arange(self.y0, self.y1, step):
                x = m * y + b
                for tx in np.arange(x - self.thickness / 2, x + self.thickness / 2, 1):
                    canvas.put_pixel(tx, y, self.color)
        else:
            m = dy / dx
            b = self.y0 - m * self.x0
            step = 1 if self.x0 < self.x1 else -1
            for x in np.arange(self.x0, self.x1, step):
                y = m * x + b
                for ty in np.arange(y - self.thickness / 2, y + self.thickness / 2, 1):
                    canvas.put_pixel(x, ty, self.color)
