import png


class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[(0, 0, 0) for _ in range(width)]
                       for _ in range(height)]

    def put_pixel(self, x, y, color):
        self.pixels[y][x] = color

    def get_merged_rows(self):
        """Converts 2d array of pixels into an array of pixel 'rows' compatible with the png writer."""
        rows = []
        for row in self.pixels:
            merged_row = ()
            for pixel in row:
                merged_row = merged_row + pixel
            rows.append(merged_row)
        return rows

    def dump_to_png(self, output_path):
        """Dumps 2d array of pixels into a png file given as an argument."""
        writer = png.Writer(self.width, self.height, greyscale=False)
        with open(output_path, 'wb') as output_file:
            writer.write(output_file, self.get_merged_rows())


if __name__ == '__main__':
    a = Canvas(3, 2)

    a.put_pixel(0, 0, 255, 165, 3)
    a.put_pixel(2, 1, 255, 255, 3)

    for bb in a.pixels:
        print(bb)

    a.dump_to_png('test.png')
