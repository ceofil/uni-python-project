import png


class Canvas:
    """
    This class represents a wrapper over a 2d array of pixels.

    Attributes:
        left, top, right, bottom: integer on-screen boundaries
        width, height: dimensions of the pixel array
        _pixels: 2d array containing elements of type (int, int, int).
    """
    def __init__(self, view_box):
        """Constructor for Canvas class.

        Args:
            view_box: 4-int tuple representing the on-screen boundaries.
        """
        self.left, self.top, self.right, self.bottom = view_box
        self.width = self.right - self.left
        self.height = self.bottom - self.top
        self._pixels = [[(0, 0, 0, 0) for _ in range(self.width)]
                        for _ in range(self.height)]

    def put_pixel(self, x, y, color):
        """Sets pixel at giver screen coords to a given color.

        Args:
            x, y: screen coords
            color: rgb color
        """
        if self.left <= x < self.right and self.top <= y < self.bottom:
            x, y = int(x - self.left), int(y - self.top)
            self._pixels[y][x] = (*color, 255)

    def get_merged_rows(self):
        """Converts 2d array of pixels into an array of pixel 'rows' compatible with the png writer."""
        rows = []
        for row in self._pixels:
            merged_row = ()
            for pixel in row:
                merged_row = merged_row + pixel
            rows.append(merged_row)
        return rows

    def dump_to_png(self, output_path):
        """Dumps 2d array of pixels into a png file given as an argument."""
        writer = png.Writer(self.width, self.height, greyscale=False, alpha=True)
        with open(output_path, 'wb') as output_file:
            writer.write(output_file, self.get_merged_rows())


if __name__ == '__main__':
    pass
